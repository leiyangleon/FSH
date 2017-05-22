# This is the Python script for the generation of the final mosaic map of FSH
# Yang Lei, Jet Propulsion Labortary, California Institute of Technology
# May 18, 2017

import xml.etree.ElementTree as ET
from numpy import *
import scipy.io as sio
import commands
import os
import time
import argparse
import pdb
from osgeo import gdal, osr
import string

def create_mosaic(directory,mosaicfile,listoffiles):

        print (time.strftime("%H:%M:%S"))
##        pdb.set_trace()

        commands.getoutput('gdalbuildvrt -separate -srcnodata 255 -overwrite '+directory+'mosaic.vrt '+listoffiles)
        commands.getoutput('gdal_translate -of GTiff -a_nodata 255 '+directory+'mosaic.vrt '+directory+'mosaic.tif')

        # Load mosaic.tif and associated parameters - .tif
        driver = gdal.GetDriverByName('GTiff')
        driver.Register()
        img = gdal.Open(directory + 'mosaic.tif')
        ref_data = array(img.ReadAsArray())
        refgeotrans = img.GetGeoTransform()
        corner_lon = refgeotrans[0]
        post_lon = refgeotrans[1]
        corner_lat = refgeotrans[3]
        post_lat = refgeotrans[5]
        geo_width = img.RasterXSize
        geo_lines = img.RasterYSize

        ######################## average all of the overlapping pixels at the same area
        ref_data = single(ref_data)
        ref_data[ref_data==255] = NaN
        avg = nanmean(ref_data,axis=0)
        avg[isnan(avg)] = 255
##        ref_data = int(ref_data)
        
        ################## Create the final GeoTiff 
        driver = gdal.GetDriverByName('GTiff')
    
        outRaster = driver.Create(directory+mosaicfile, geo_width, geo_lines)
        outRaster.SetGeoTransform([corner_lon, post_lon, 0, corner_lat, 0, post_lat])
        outband = outRaster.GetRasterBand(1)

        outband.WriteArray(avg)
        outRasterSRS = osr.SpatialReference()
        outRasterSRS.ImportFromEPSG(4326)
        outRaster.SetProjection(outRasterSRS.ExportToWkt())
        outband.FlushCache()

        print (time.strftime("%H:%M:%S"))


        print "Final mosaic generation done !!!"





        
parser = argparse.ArgumentParser(description="Create final mosaic map of forest stand height")
parser.add_argument('directory', type=str, help='the same root directory as forest_stand_height.py executes')
parser.add_argument('mosaicfile', type=str, help='file name of the final mosaic file')
parser.add_argument('listoffiles', type=str, help='paths to all the forest height maps that are to be combined')



args = parser.parse_args()

print "\n"
print args
print "\n"

create_mosaic(args.directory,args.mosaicfile,args.listoffiles)
