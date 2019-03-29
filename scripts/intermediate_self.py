# intermediate_self.py
# Tracy Whelen, Microwave Remote Sensing Lab, University of Massachusetts
# December 8, 2015
# Yang Lei, Jet Propulsion Labortary, California Institute of Technology
# May 18, 2017


# This script is the python version of intermediate_self.m, which calculates the overlap area
# between the LiDAR and the central scene.

#!/usr/bin/python

from numpy import *
import scipy.io as sio
import json
from scipy.interpolate import griddata
from osgeo import gdal
import flag_scene_file as fsf
import remove_nonforest as rnf

# Define intermediate_self function
# Input parameters are the central scene, the flag-scene data file, non-forest maskfile, reference data file, and the file directory
def intermediate_self(start_scene, flagfile, ref_file, maskfile, directory):
   
    # Set scene data, file name, and image folder name
    scene2_data = fsf.flag_scene_file(flagfile, start_scene, directory)
    filename2 = scene2_data[1]
    image_folder = "f" + scene2_data[4] + "_o" + scene2_data[5] + "/"

    # Set D constant --- D = 1 arc second, this parameter is based on the use of ALOS data
    #D = 8.3333333 * (10**-4)
    D = 2.77777778 * (10**-4)  #for tracy test case
    
#    # Load image file and associated parameters -- .mat/gamma version
#    # kz must be extracted from the array
#    file2 = sio.loadmat(directory + filename2 + '.mat')
#    corr2 = file2['corr_vs']
#    kz2 = file2['kz'][0][0]
#    coords2 = file2['coords'][0]
    
    # Load central image file and associated parameters

    file2 = sio.loadmat(directory + image_folder + filename2 + "_orig.mat")
    corr2 = file2['corr_vs']
    kz2 = file2['kz'][0][0]
    coords2 = file2['coords'][0]
    
##    file2 = open(directory + image_folder + filename2 + "_orig.json")
##    file2_data = json.load(file2)
##    file2.close()
##    # Set parameter values based on file2_data   
##    corr2 = array(file2_data[0])
##    kz2 = float(file2_data[1])
##    coords2 = array(file2_data[2])

    # Remove non-forest from the image
    if maskfile != '-':
        corr2 = rnf.remove_nonforest(corr2, coords2, maskfile, directory)
    
    # Load LiDAR files and associated parameters - .tif
    driver = gdal.GetDriverByName('GTiff')
    driver.Register()
    img = gdal.Open(directory + ref_file)
    ref_data = array(img.ReadAsArray())
    refgeotrans = img.GetGeoTransform()
    corner_lon = refgeotrans[0]
    post_lon = refgeotrans[1]
    corner_lat = refgeotrans[3]
    post_lat = refgeotrans[5]
    width = img.RasterXSize
    lines = img.RasterYSize
    
    # Set LiDAR parameters into correct format
    corr1 = ref_data.transpose()
    corr1[corr1 < 0] = NaN   # set margin areas to NaN
    coords1 = array([corner_lat, corner_lat + (lines * post_lat), corner_lon, corner_lon + (width * post_lon)])
    
    # Set the image boundaries
    north1 = coords1[0]
    south1 = coords1[1]
    west1 = coords1[2]
    east1 = coords1[3]
    north2 = coords2[0]
    south2 = coords2[1]
    west2 = coords2[2]
    east2 = coords2[3]

    # Determine boundaries of the overlap area
    overlap_north = min(north1, north2)
    overlap_south = max(south1, south2)
    overlap_east = min(east1, east2)
    overlap_west = max(west1, west2)

    # Calculate overlap boundaries in coordinates of image2 (ex image1[1000-1200] vs image2[0-200])
    xw2 = int(round(((overlap_west - west2) / D) + 1))
    xe2 = int(round(((overlap_east - west2) / D) + 1))
    xn2 = int(round((-(overlap_north - north2) / D) + 1))
    xs2 = int(round((-(overlap_south - north2) / D) + 1))
  
    # Set overlap sections for the LiDAR and SAR images
    I1 = corr1.copy()
    I2 = corr2[xw2-1:xe2][:, xn2-1:xs2]


    # Set average S and C parameters based on the average S and C (0<s<1, 0<c<20 so s=0.65 and c=13)
    S_param2 = 0.65
    C_param2 = 13

    # Create grid for image1
    [Dy1, Dx1] = I1.shape
    x1 = linspace(0, 1, Dx1)
    y1 = linspace(0, 1, Dy1)
    [X1, Y1] = meshgrid(x1, y1)
    
    # Create grid for image2
    [Dy2, Dx2] = I2.shape    
    x2 = linspace(0, 1, Dx2)
    y2 = linspace(0, 1, Dy2)
    [X2, Y2] = meshgrid(x2, y2)

    # Set NaN values to -100 to avoid interpolation errors
    I1[isnan(I1)] = -100
    I2[isnan(I2)] = -100
    

    # Co-register the two images
##    I1 = griddata((X1.flatten(), Y1.flatten()), I1.flatten(), (X2, Y2), method='nearest')
    I2 = griddata((X2.flatten(), Y2.flatten()), I2.flatten(), (X1, Y1), method='nearest')

    # Reset NaN values
    IND1 = (I1 == -100)
    IND2 = (I2 == -100)
    IND = logical_or(IND1, IND2)
    I1[IND] = NaN
    I2[IND] = NaN

    # Save link file using JSON
    # linkfilename = "self.json"
    # linkfile = open(directory + "output/" + linkfilename, 'w')
    # json.dump([I1.tolist(), I2.tolist(), S_param2, C_param2], linkfile)
    # linkfile.close()
    
    # Save link file using JSON
    linkfilename = "self.mat"
    linkfile = directory + "output/" + linkfilename
    sio.savemat(linkfile,{'I1':I1,'I2':I2})
    
    
