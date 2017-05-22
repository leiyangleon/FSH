# forest_disturbance.py
# Yang Lei, Jet Propulsion Labortary, California Institute of Technology
# May 18, 2017

# This script calls all the processing steps needed to take ROI_PAC output and create a map of tree heights.

#!/usr/bin/python
from numpy import *
import time
import pdb
import json
import argparse
import commands
import string
import xml.etree.ElementTree as ET
from scipy import signal
import argparse
import scipy.io as sio
import json
from osgeo import gdal, osr
import simplekml
from PIL import Image
import os.path
import math as mt
import remove_corr_bias as rcb
from scipy.signal import medfilt2d




# Define forest_stand_height function
# Input parameters are scenes, edges, start scene, iterations, link file, flag file, reference data file, file directory, 
    # list of all output tree height map file types, averaging numbers in lat and lon for "self" and "pairwise" fitting, 
    # averaging numbers in lat and lon for "self" and "pairwise" error calculation, bin_size for density calculation in scatter plot fitting, 
    # flag for sparse data cloud filtering, flag for exporting the disturbance maps, flag for exporting the json error metric files (for all flags 0 is no output, 1 is output)

def forest_disturbance_ISCE(file_directory, win=3, numLooks=20, noiselevel=0.0, flag_grad=0):

    print (time.strftime("%H:%M:%S"))

    # Set error warnings to ignore "invalid value" warnings caused by NaN values
    seterr(invalid='ignore')


    # Extract ISCE parameters
    logfile = file_directory+"isce.log"

    strg=commands.getoutput('fgrep "master.instrument.range_pixel_size" '+logfile)
    range_pixel_res = float(string.split(strg)[-1])

    strg=commands.getoutput('fgrep "master.instrument.radar_wavelength" '+logfile)
    llambda = float(string.split(strg)[-1])

    strg=commands.getoutput('fgrep "starting_range" '+logfile)
    first_range = float(string.split(strg)[string.split(strg).__len__()/2-1])
    strg=commands.getoutput('fgrep "master.width" '+logfile)
    num_range_bin = float(string.split(strg)[-1])
#    num_range_bin = float(string.split(strg)[string.split(strg).__len__()/2-1])
    center_range = first_range + (num_range_bin/2-1)*range_pixel_res

    strg=commands.getoutput('fgrep "master.instrument.incidence_angle" '+logfile)
    incid_angle = float(string.split(strg)[-1])

    strg=commands.getoutput('fgrep "baseline.perp_baseline" '+logfile)
    baseline = (float(string.split(strg)[string.split(strg).__len__()/2-1])+float(string.split(strg)[string.split(strg).__len__()-1]))/2

    xmlfile = file_directory+"topophase.cor.geo.xml"
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    delta_array = array([])
    start_array = array([])
    size_array = array([])
    size_array.dtype = int
    for size in root.iter('property'):
        if size.items()[0][1] == 'size':
            size_array = append(size_array, int(float(size.find('value').text)))
    for delta_val in root.iter('property'):
        if delta_val.items()[0][1] == 'delta':
            delta_array = append(delta_array, float(delta_val.find('value').text))
    for start_val in root.iter('property'):
        if start_val.items()[0][1] == 'startingvalue':
            start_array = append(start_array, float(start_val.find('value').text))   
    end_array = start_array + size_array * delta_array
    north = max(start_array[1],end_array[1])
    south = min(start_array[1],end_array[1])
    east = max(start_array[0],end_array[0])
    west = min(start_array[0],end_array[0])
    coords = [north, south, west, east]
    geo_width = size_array[0]
    geo_nlines = size_array[1]
    corner_lat = north
    corner_lon = west
    step_lat = delta_array[1]
    step_lon = delta_array[0]

    xmlfile = file_directory+"resampOnlyImage.amp.geo.xml"
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    delta_array = array([])
    start_array = array([])
    size_array = array([])
    size_array.dtype = int
    for size in root.iter('property'):
        if size.items()[0][1] == 'size':
            size_array = append(size_array, int(float(size.find('value').text)))
    if (size_array[0]<geo_width)|(size_array[1]<geo_nlines):
        for delta_val in root.iter('property'):
            if delta_val.items()[0][1] == 'delta':
                delta_array = append(delta_array, float(delta_val.find('value').text))
        for start_val in root.iter('property'):
            if start_val.items()[0][1] == 'startingvalue':
                start_array = append(start_array, float(start_val.find('value').text))   
        end_array = start_array + size_array * delta_array
        north = max(start_array[1],end_array[1])
        south = min(start_array[1],end_array[1])
        east = max(start_array[0],end_array[0])
        west = min(start_array[0],end_array[0])
        coords = [north, south, west, east]
        geo_width = size_array[0]
        geo_nlines = size_array[1]
        corner_lat = north
        corner_lon = west
        step_lat = delta_array[1]
        step_lon = delta_array[0]
    

    # Read geolocated amp and cor files

    fid_cor = open(file_directory + "topophase.cor.geo", "rb")
    cor_file = fromfile(fid_cor, dtype=dtype('<f'))
##    pdb.set_trace()
    corr = cor_file.reshape(2*geo_width, -1, order='F')
    corr = corr[:,0:geo_nlines]
    corr_mag = corr[geo_width:2*geo_width,:]
    avg_inty = corr[0:geo_width,:]
    

    fid_amp = open(file_directory + "resampOnlyImage.amp.geo", "rb")
    amp_file = fromfile(fid_amp, dtype=dtype('<f'))
    inty = amp_file.reshape(2*geo_width, -1, order='F')
    inty = inty[:,0:geo_nlines]
    inty1 = inty[::2,:]
    inty2 = inty[1::2,:]

    inty1[inty1 <= 0] = NaN
    inty2[inty2 <= 0] = NaN
    corr_mag[corr_mag <= 0] = NaN  


################### Noise level for ISCE-processed SAR backscatter power output
    if noiselevel == 0.0:
        ####### ALOS thermal noise level
        N1 = 55.5**2
        N2 = 55.5**2
    else:
        N1 = noiselevel
        N2 = noiselevel


############ ALOS2 WMNF
##    noiselevel = (9.1*10**4)**2
############ ALOS2 ME
##    noiselevel = (4.2*10**4)**2



    # Operations
    inty1 = power(inty1,2)                   # Hardcoded based on 2 range looks and 10 azimuth looks
    inty2 = power(inty2,2) 

    S1 = inty1 - N1
    g_th_1 = zeros(S1.shape)
    g_th_1[S1>N1] = sqrt(S1[S1>N1] / (S1[S1>N1] + N1))
    g_th_1[isnan(S1)] = NaN
    g_th_1[S1 <= N1] = NaN
    
    S2 = inty2-N2
    g_th_2 = zeros(S2.shape)
    g_th_2[S2>N2] = sqrt(S2[S2>N2] / (S2[S2>N2] + N2))
    g_th_2[isnan(S2)] = NaN
    g_th_2[S2 <= N2] = NaN
    
    g_th = g_th_1 * g_th_2

    corr_mag[corr_mag<0] = 0
    corr_mag[corr_mag>1] = 1
    corr_mag = rcb.remove_corr_bias(corr_mag,numLooks)
    corr_mag[corr_mag<0] = 0
    
    corr_vs = corr_mag / g_th

    
    # set constants
    pi=mt.pi

##    latshift = 13.25 / 60 / 60
##    longshift = 5.16 / 60 / 60
##    coords = array(coords)
##    coords[0:2] = coords[0:2] - latshift
##    coords[2:4] = coords[2:4] - longshift
##    coords = coords.tolist()

    
    
    # correcting geometric decorrelation related to value compensation of ROI result compared to GAMMA. Caused by baseline/other decorrelation    
    gamma_base = 1 - (2 * mt.fabs(baseline) * mt.cos(incid_angle / 180 * pi) * range_pixel_res / mt.sin(incid_angle / 180 * pi) / llambda / center_range)
    gamma_geo = gamma_base
    corr_vs = corr_vs / gamma_geo                         
    corr_vs[corr_vs>1] = 1

    #################### Simple Radiometric correction of the coherences
    if flag_grad == 1:
        y = np.linspace(1, geo_width, geo_width)
        x = np.linspace(1, geo_nlines, geo_nlines)
        [X, Y] = np.meshgrid(x, y)
        A = np.vstack([X[~np.isnan(corr_vs)], Y[~np.isnan(corr_vs)], np.ones(np.size(corr_vs[~np.isnan(corr_vs)]))]).T
        coeff = np.linalg.lstsq(A, corr_vs[~np.isnan(corr_vs)])[0]
        corr_vs = corr_vs - X*coeff[0] - Y*coeff[1]
        corr_vs[corr_vs>1] = 1
        corr_vs[corr_vs<0] = 0
    

    ##################### Correct for temporal decorrelation
    bin_size = 500
    IND = (avg_inty > 5 * sqrt(N1))
    corr_hist = corr_vs[IND&(corr_vs > 0.1)]
    hist, bin_edges = histogram(corr_hist[~isnan(corr_hist)],bins=bin_size)

    bin_center = (bin_edges[0:bin_size] + bin_edges[1:(bin_size+1)]) / 2
        
    temp_decor = bin_center[argmax(hist)]

    corr_avg = mean(corr_vs[~isnan(corr_vs)])

    corr_vs1 = corr_vs / temp_decor

    print 'Scene-wide mean correlation: '+str(corr_avg)
    print 'Forest mean temporal correlation: '+str(temp_decor)

    corr_vs1 = medfilt2d(corr_vs1, kernel_size=win)

    corr_vs1[corr_vs1>1] = 1
    corr_vs1[corr_vs1<0] = 0
    
    kz = -2 * pi * 2 / llambda / center_range / mt.sin(incid_angle/180*pi) * baseline
    kz = mt.fabs(kz)

    corr_vs = corr_vs.transpose()
    corr_vs1 = corr_vs1.transpose()

    ################## Create the GeoTiff 
    driver = gdal.GetDriverByName('GTiff')
    
    outRaster = driver.Create(file_directory+"uncorrected_corr_map.tif", geo_width, geo_nlines, 1, gdal.GDT_Float32)
    outRaster.SetGeoTransform([corner_lon, step_lon, 0, corner_lat, 0, step_lat])
    outband = outRaster.GetRasterBand(1)

    outband.WriteArray(corr_vs)
    outRasterSRS = osr.SpatialReference()
    outRasterSRS.ImportFromEPSG(4326)
    outRaster.SetProjection(outRasterSRS.ExportToWkt())
    outband.FlushCache()

    ################## Create the GeoTiff 
    driver = gdal.GetDriverByName('GTiff')
    
    outRaster = driver.Create(file_directory+"corrected_corr_map.tif", geo_width, geo_nlines, 1, gdal.GDT_Float32)
    outRaster.SetGeoTransform([corner_lon, step_lon, 0, corner_lat, 0, step_lat])
    outband = outRaster.GetRasterBand(1)

    outband.WriteArray(corr_vs1)
    outRasterSRS = osr.SpatialReference()
    outRasterSRS.ImportFromEPSG(4326)
    outRaster.SetProjection(outRasterSRS.ExportToWkt())
    outband.FlushCache()

    ################## Create the GeoTiff 
    driver = gdal.GetDriverByName('GTiff')
    
    outRaster = driver.Create(file_directory+"disturbance_map.tif", geo_width, geo_nlines, 1, gdal.GDT_Float32)
    outRaster.SetGeoTransform([corner_lon, step_lon, 0, corner_lat, 0, step_lat])
    outband = outRaster.GetRasterBand(1)

    dist = 1 - corr_vs1
    outband.WriteArray(dist)
    outRasterSRS = osr.SpatialReference()
    outRasterSRS.ImportFromEPSG(4326)
    outRaster.SetProjection(outRasterSRS.ExportToWkt())
    outband.FlushCache()

    sio.savemat(file_directory+'KZ.mat',{'kz':kz})
    sio.savemat(file_directory+'coh.mat',{'temp_decor':temp_decor,'corr_avg':corr_avg})
    
        
# Gather parameters from the command line and run the function   
parser = argparse.ArgumentParser(description="Run Forest Stand Height module")
parser.add_argument('file_directory', type=str, help='path of the file directory, make sure to finish with a slash to separate final directory and file')
parser.add_argument('win', type=int, help='median filter window size', default=3)
parser.add_argument('--numLooks', type=int, nargs='?', default=20)
parser.add_argument('--noiselevel', type=float, nargs='?', default=0.0)
parser.add_argument('--flag_grad', type=int, choices=[0, 1], nargs='?', default=0)


args = parser.parse_args()

print "\n"
print args
print "\n"

forest_disturbance_ISCE(args.file_directory, args.win, args.numLooks, args.noiselevel, args.flag_grad)
