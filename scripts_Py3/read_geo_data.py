# read_geo_data.py
# Tracy Whelen, Microwave Remote Sensing Lab, University of Massachusetts
# November 16, 2015
# Simon Kraatz, UMass Amherst
# April 28, 2020

# This script reads lat/long, step(pixel) size, and image size from either a geotiff or a text file based on ROI_PAC output

#!/usr/bin/python
from osgeo import gdal
import pdb
import os

# Define read_geo_data function
# Input parameters are the filename of the input geodata file, and the file directory
def read_geo_data(coord_file, directory):
    
    # Set filename for file to be searched
    filename = os.path.join(directory, coord_file)

##    pdb.set_trace()
    
    # Read parameters based on file type GeoTIFF or ROI_PAC text file)
    if(coord_file[-3:] == "tif"):
        # Read GeoTIFF
        driver = gdal.GetDriverByName('GTiff')
        driver.Register()
        image = gdal.Open(filename)
        refgeotrans = image.GetGeoTransform()
        corner_long = refgeotrans[0]
        post_long = refgeotrans[1]
        corner_lat = refgeotrans[3]
        post_lat = refgeotrans[5]
        width = image.RasterXSize
        nlines = image.RasterYSize
        
    else:
        # Read ROI_PAC text file
        for line in open(filename):
            if line.startswith("width"):
                width = int(line.strip().split()[1])
            elif line.startswith("nlines"):
                nlines = int(line.strip().split()[1])
            elif line.startswith("corner_lat"):
                corner_lat = float(line.strip().split()[1])
            elif line.startswith("corner_lon"):
                corner_long = float(line.strip().split()[1])
            elif line.startswith("post_lat"):
                post_lat = float(line.strip().split()[1])
            elif line.startswith("post_lon"):
                post_long = float(line.strip().split()[1])
            
    return width, nlines, corner_lat, corner_long, post_lat, post_long
