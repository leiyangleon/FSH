# auto_tree_height_single_ISCE.py
# Yang Lei, Jet Propulsion Labortary, California Institute of Technology
# May 18, 2017

# This script extracts the correlation values, kz value, corner coordinates, and geodata from the ISCE output files.

#!/usr/bin/python
import numpy as np
import math as mt
import read_rsc_data as rrd
import remove_corr_bias as rcb
import subprocess
import string
import xml.etree.ElementTree as ET
import pdb
from scipy import signal


# Define auto_tree_height_single function
# Input parameters are the file directory, and the names of the two image files
def auto_tree_height_single_ISCE(directory, date1, date2, numLooks, noiselevel, flag_grad):


    # Extract ISCE parameters
    logfile = directory+"int_"+date1+"_"+date2+"/isce.log"

    strg=subprocess.getoutput('fgrep "master.instrument.range_pixel_size" '+logfile)
    range_pixel_res = float(strg.split()[-1])

    strg=subprocess.getoutput('fgrep "master.instrument.radar_wavelength" '+logfile)
    llambda = float(strg.split()[-1])

    strg=subprocess.getoutput('fgrep "runTopo.inputs.range_first_sample" '+logfile)
    first_range = float(strg.split()[-1])
    strg=subprocess.getoutput('fgrep "runTopo.inputs.width" '+logfile)
    num_range_bin = int(strg.split()[-1])
    strg=subprocess.getoutput('fgrep "runTopo.inputs.number_range_looks" '+logfile)
    num_range_looks = int(strg.split()[-1])
    center_range = first_range + (num_range_bin/2-1)*range_pixel_res*num_range_looks
##    strg=commands.getoutput('fgrep "SLC Starting Range" '+logfile)
##    first_range = float(strg.split()[strg.split().__len__()/2-1])
##    strg=commands.getoutput('fgrep "SLC width" '+logfile)
##    num_range_bin = float(strg.split()[strg.split().__len__()/2-1])
##    center_range = first_range + (num_range_bin/2-1)*range_pixel_res

    strg=subprocess.getoutput('fgrep "master.instrument.incidence_angle" '+logfile)
    incid_angle = float(strg.split()[-1])


    strg=subprocess.getoutput('fgrep "baseline.perp_baseline" '+logfile)


    baseline = (float(strg.split()[int(strg.split().__len__()/2-1)])+float(strg.split()[int(strg.split().__len__()-1)]))/2

    print (baseline)
    

    xmlfile = directory+"int_"+date1+"_"+date2+"/topophase.cor.geo.xml"
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    delta_array = np.array([])
    start_array = np.array([])
    size_array = np.array([], dtype=np.int32)
    for size in root.iter('property'):
        if size.items()[0][1] == 'size':
            size_array = np.append(size_array, int(size.find('value').text))
    for delta_val in root.iter('property'):
        if delta_val.items()[0][1] == 'delta':
            delta_array = np.append(delta_array, float(delta_val.find('value').text))
    for start_val in root.iter('property'):
        if start_val.items()[0][1] == 'startingvalue':
            start_array = np.append(start_array, float(start_val.find('value').text))
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

    xmlfile = directory+"int_"+date1+"_"+date2+"/resampOnlyImage.amp.geo.xml"
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    delta_array = np.array([])
    start_array = np.array([])
    size_array = np.array([], dtype=np.int32)
    for size in root.iter('property'):
        if size.items()[0][1] == 'size':
            size_array = np.append(size_array, int(size.find('value').text))
    if (size_array[0]<geo_width)|(size_array[1]<geo_nlines):
        for delta_val in root.iter('property'):
            if delta_val.items()[0][1] == 'delta':
                delta_array = np.append(delta_array, float(delta_val.find('value').text))
        for start_val in root.iter('property'):
            if start_val.items()[0][1] == 'startingvalue':
                start_array = np.append(start_array, float(start_val.find('value').text))
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

    fid_cor = open(directory + "int_"+date1+"_"+date2+"/topophase.cor.geo", "rb")
    cor_file = np.fromfile(fid_cor, dtype=np.dtype('<f'))
##    pdb.set_trace()
    corr = cor_file.reshape(2*geo_width, -1, order='F')
    corr = corr[:,0:geo_nlines]
    corr_mag = corr[geo_width:2*geo_width,:]

    fid_amp = open(directory + "int_"+date1+"_"+date2+"/resampOnlyImage.amp.geo", "rb")
    amp_file = np.fromfile(fid_amp, dtype=np.dtype('<f'))
    inty = amp_file.reshape(2*geo_width, -1, order='F')
    inty = inty[:,0:geo_nlines]
    inty1 = inty[::2,:]
    inty2 = inty[1::2,:]


    # Operations
    inty1 = np.power(inty1,2)                   # Hardcoded based on 2 range looks and 10 azimuth looks
    inty2 = np.power(inty2,2)

    inty1[inty1 <= 0] = np.NaN
    inty2[inty2 <= 0] = np.NaN
    corr_mag[corr_mag <= 0] = np.NaN

################### Noise level for ISCE-processed SAR backscatter power output
    if noiselevel == 0.0:
        ####### ALOS thermal noise level
        N1 = 55.5**2
        N2 = 55.5**2
    else:
        N1 = noiselevel
        N2 = noiselevel


    S1 = inty1 - N1
    g_th_1 = np.zeros(S1.shape)
    g_th_1[S1>N1] = np.sqrt(S1[S1>N1] / (S1[S1>N1] + N1))
    g_th_1[np.isnan(S1)] = np.NaN
    g_th_1[S1 <= N1] = np.NaN

    S2 = inty2-N2
    g_th_2 = np.zeros(S2.shape)
    g_th_2[S2>N2] = np.sqrt(S2[S2>N2] / (S2[S2>N2] + N2))
    g_th_2[np.isnan(S2)] = np.NaN
    g_th_2[S2 <= N2] = np.NaN

    g_th = g_th_1 * g_th_2

    corr_mag[corr_mag<0] = 0
    corr_mag[corr_mag>1] = 1
    corr_mag = rcb.remove_corr_bias(corr_mag,numLooks)
    corr_mag[corr_mag<0] = 0

    corr_vs = corr_mag / g_th


##    # force margin to be nans
##    IND = np.double(~np.isnan(corr_vs))
##    mask_size = 100
##    mask = np.ones((mask_size,mask_size))
##    IND1 = signal.convolve2d(IND, mask, boundary='symm', mode='same')/mask_size**2
##    IND = ~(IND1==1.0)
##    corr_vs[IND] = np.NaN


    # set constants
    pi=mt.pi

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

    kz = -2 * pi * 2 / llambda / center_range / mt.sin(incid_angle/180*pi) * baseline
    kz = mt.fabs(kz)

    # Return corr_vs, kz, coords
    return corr_vs, kz, coords, geo_width, geo_nlines, corner_lat, corner_lon, step_lat, step_lon
