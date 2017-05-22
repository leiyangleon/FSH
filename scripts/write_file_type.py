# write_file_type.py
# Tracy Whelen, Microwave Remote Sensing Lab, University of Massachusetts
# November 17, 2015
# Yang Lei, Jet Propulsion Labortary, California Institute of Technology
# May 18, 2017


# This script writes the input array (the tree height map or diff_height map) to a file, with the file type depending on input parameters.
# Current output types are: .gif, .json, .kml, .mat, .tif (input without the "." so that ".kml" becomes "kml")
#!/usr/bin/python

from numpy import *
import scipy.io as sio
import json
from osgeo import gdal, osr
import simplekml
from PIL import Image
import os.path
import read_geo_data as rgd
import pdb

# Define write_file_type function
# Input parameters are the array, output type (ex. stand height, diff_height, etc), output filename, output directory, and file type (inputted as a string of the file extension)
def write_file_type(data, outtype, filename, directory, filetype, coords, ref_file=""):
    
#    print "orig filename = " + filename
    
    # Use if/else to determine the desired type of file output
    if(filename[-8:] == "_255_255"):
        outfilename = filename[:-4]
    elif((filename[-4:] == "_fsh") or (filename[-5:] == "_diff") or (filename[-4:] == "_255")):
        outfilename = filename
    else:
        if(outtype == "stand_height"):
            outfilename = filename + "_fsh"
        elif(outtype == "diff_height"):
            outfilename = filename + "_diff"
            
#    print "outfilename = " + outfilename + "\n"
    
    # Use if/else to determine the desired type of file output    
    # Create .gif output
    if(filetype == "gif"):
        # Check if a 0-255 .tif with the same filename already exists, and if not create it.
        if (os.path.isfile(directory + outfilename + "_255.tif") == True):
            gif_img = Image.open(directory + outfilename + "_255.tif")
        else:
            # Set array in a 0-255 range for gif/kml
            # Get dimensions of array and then flatten for use with nonzero()
            (row, col) = data.shape
            data = data.flatten()
            # Get the nonzero indices and min/max
            nz_IND = nonzero(data)
            nz_min = data[nz_IND[0]].min()
            nz_max = data[nz_IND[0]].max()
            # Set the scaled values
            data255 = data.copy()
            data255[nz_IND[0]] = (data[nz_IND[0]] - nz_min) * (255 / (nz_max - nz_min)) + 1
            # Reshape the array of scaled values
            data255 = reshape(data255, (row, col))
            data = reshape(data, (row, col))
            
            # Write 0-255 .tif
            write_file_type(data255, outtype, outfilename + "_255", directory, "tif", coords, ref_file)
            gif_img = Image.open(directory + outfilename + "_255.tif")
            
        # Create the .gif
        gif_img.save(directory + outfilename + "_255.gif", "GIF", transparency=0)
        
    # Create .json output    
    elif(filetype == "json"):
        jsonfile = open(directory + outfilename + '.json', 'w')
        json.dump([data.tolist()], jsonfile)
        jsonfile.close()
        
    # Create .kml output        
    elif(filetype == "kml"):
        # Determine the realname based on whether or not a single image is being processed or a pair
        if(filename[3] == "_"):   # pair
            realname = filename[:31]
        else:
            realname = filename[:23]
        
##        realname = filename
        
        # Read geo location information in from a text or geotiff file depending on outtype
        if(outtype == "stand_height"):
            (width, lines, north, west, lat_step, long_step) = rgd.read_geo_data(realname + "_geo.txt", directory)
            north = coords[0]
            west = coords[2]
            south = coords[1]
            east = coords[3]
        elif(outtype == "diff_height"):
            (width, lines, north, west, lat_step, long_step) = rgd.read_geo_data(ref_file, directory[:-10])
            south = north + (lat_step * lines)
            east = west + (long_step * width)
       
        
##        lat_step = -2.77777777778 * (10**-4)
##        long_step = 2.77777777778 * (10**-4)
        


        # Check if a .gif with the same filename does not already exist then create it.
        if (os.path.isfile(directory + outfilename + "_255.gif") == False):
            write_file_type(data, outtype, outfilename, directory, "gif", coords, ref_file)            
            
        # Create the .kml
        kml = simplekml.Kml()
        arraykml = kml.newgroundoverlay(name=outfilename)
        arraykml.icon.href = directory + outfilename + "_255.gif"
        arraykml.latlonbox.north = north
        arraykml.latlonbox.south = south
        arraykml.latlonbox.east = east
        arraykml.latlonbox.west = west
        kml.save(directory + outfilename + "_255.kml")
    
    # Create .mat output
    elif(filetype == "mat"):
        sio.savemat(directory + outfilename + '.mat', {'data':data})

    # Create .tif output
    elif(filetype == "tif"):
        # Determine the realname based on whether or not a single image is being processed or a pair
        if(filename[3] == "_"):   # pair
            realname = filename[:31]
        else:
            realname = filename[:23]

##        realname = filename
        
        # Read geo location information in from a text or geotiff file depending on outtype
        if(outtype == "stand_height"):
            (cols, rows, corner_lat, corner_long, lat_step, long_step) = rgd.read_geo_data(realname + "_geo.txt", directory)
            corner_lat = coords[0]
            corner_long = coords[2]
            lat_step = -2.77777777778 * (10**-4)
            long_step = 2.77777777778 * (10**-4)
        elif(outtype == "diff_height"):
            (cols, rows, corner_lat, corner_long, lat_step, long_step) = rgd.read_geo_data(ref_file, directory[:-10])
            selffile_data = sio.loadmat(directory[:-10] + "output/" + "self.mat")
            image1 = selffile_data['I1']
            cols = int(image1.shape[0])
            rows = int(image1.shape[1])
            lat_step = -2.77777778 * (10**-4)
            long_step = 2.77777778 * (10**-4)
#            pdb.set_trace()

        # Create the GeoTiff 
        driver = gdal.GetDriverByName('GTiff')
        outRaster = driver.Create(directory + outfilename + ".tif", cols, rows)
#        outRaster = driver.Create(directory + outfilename + ".tif", cols, rows, 1, gdal.GDT_Float32)
        outRaster.SetGeoTransform([corner_long, long_step, 0, corner_lat, 0, lat_step])
        outband = outRaster.GetRasterBand(1)
        outband.WriteArray(data)
        outRasterSRS = osr.SpatialReference()
        outRasterSRS.ImportFromEPSG(4326)
        outRaster.SetProjection(outRasterSRS.ExportToWkt())
        outband.FlushCache()
    
    else:
        # Error message
        print "Error: The selected file type is invalid. Please try again and choose a different output format."
        print "You selected %s" % filetype
        print "File types available: .gif, .json, .kml, .mat, .tif -- input without the ., such as kml instead of .kml\n"
