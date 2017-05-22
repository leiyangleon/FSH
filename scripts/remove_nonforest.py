# remove_nonforest.py
# Tracy Whelen, Microwave Remote Sensing Lab, University of Massachusetts
# Diya Chowdhury, Applied GeoSolutions
# October 26, 2015

# This script is the python version of remove_water.m, however it removes all
# non-forest instead of just water

#!/usr/bin/python

from numpy import *
from osgeo import gdal
import scipy.interpolate as sciint
import pdb

# Define remove_nonforest function
# Input parameters are the image, its coordinates, the non-forest maskfile, and input/output file directory
def remove_nonforest(I, func_coords, maskfile, directory):
    
    # Load mask file as a GeoTIFF
    maskfile = gdal.Open(directory + maskfile)    
    mask = array(maskfile.ReadAsArray())
    
    # Set any NaN values to 1 (aka not a forest)
    mask[isnan(mask)] = 1
    
    # Get mask geo parameters
    width = maskfile.RasterXSize
    nlines = maskfile.RasterYSize
    maskgeotrans = maskfile.GetGeoTransform()
    corner_lon = maskgeotrans[0]
    post_lon = maskgeotrans[1]
    corner_lat = maskgeotrans[3]
    post_lat = maskgeotrans[5]
    
    # Transpose mask so that it matches orientation of the radar data
    mask = mask.transpose()
    widthT = nlines
    nlinesT = width
    
    # Set coordinates based on file parameters
    file_coords = array([corner_lat, (corner_lat + (nlinesT - 1.0) * post_lat), corner_lon, (corner_lon + (widthT - 1.0) * post_lon)])
    
    # Calculate overlap boundaries in new coordinate system
    xw = round(((func_coords[2] - file_coords[2]) / post_lon) + 1)
    xe = round(((func_coords[3] - file_coords[2]) / post_lon) + 1)
    xn = round(((func_coords[0] - file_coords[0]) / post_lat) + 1)
    xs = round(((func_coords[1] - file_coords[0]) / post_lat) + 1)

    # Trim mask
    mask = logical_not(mask[xw-1:xe][:, xn-1:xs])
    
    # Get size of image and mask
    [m, n] = I.shape
    [M, N] = mask.shape
    
    # Make range of values from 0-1 based on M and N (not including 1), and run linspace
    x = linspace(0, 1, N, endpoint=False)
    y = linspace(0, 1, M, endpoint=False)
    [X, Y] = meshgrid(x, y)

    # Make range of values from 0-1 based on m and n (not including 1), and run linspace
    xp = linspace(0, 1, n, endpoint=False)
    yp = linspace(0, 1, m, endpoint=False) 
    [XP, YP] = meshgrid(xp, yp)    
    
    # Run interpolation
    O = sciint.griddata((X.flatten(), Y.flatten()), mask.flatten(), (XP, YP), method='nearest')
    O = double(O)
    O[O == 0] = NaN
    O = I * O
    return O
