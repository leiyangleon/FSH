# auto_tree_height_single_ISCE.py
# Yang Lei, Jet Propulsion Labortary, California Institute of Technology
# May 18, 2017
# Simon Kraatz, UMass Amherst
# April 28, 2020

# This script extracts the correlation values, kz value, corner coordinates, and geodata from the ISCE output files.

#!/usr/bin/python
import numpy as np
import math as mt
import read_rsc_data as rrd
import remove_corr_bias as rcb
import subprocess, os
import string
import xml.etree.ElementTree as ET
import pdb
from scipy import signal


# Define auto_tree_height_single function
# Input parameters are the file directory, and the names of the two image files
def auto_tree_height_single_ISCE(directory, date1, date2, numLooks, noiselevel, flag_grad, latshift, longshift):


    # Extract ISCE parameters
    print(date1, date2)
    xmlfilet = [f for f in os.listdir(os.path.join(directory, 'int_'+date1+'_'+date2)) if f.endswith('Proc.xml')][0]
    xmlfile = os.path.join(directory, 'int_'+date1+'_'+date2, xmlfilet)
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    root_tag = root.tag
    
    try:
        range_pixel_res = float(root.findall("./master/instrument/range_pixel_size")[0].text)
    except:
        range_pixel_res = float(root.findall("./reference/instrument/range_pixel_size")[0].text)
    try:
        llambda = float(root.findall("./master/instrument/radar_wavelength")[0].text)
    except:
        llambda = float(root.findall("./reference/instrument/radar_wavelength")[0].text)
    try:
        first_range = float(root.findall("./runTopo/inputs/range_first_sample")[0].text)
    except:
        first_range = float(root.findall("./runTopo/inputs/RANGE_FIRST_SAMPLE")[0].text)
    try:
        num_range_bin = int(root.findall("./runTopo/inputs/width")[0].text)
    except:
        num_range_bin = int(root.findall("./runTopo/inputs/WIDTH")[0].text)
    try:
        num_range_looks = int(root.findall("./runTopo/inputs/number_range_looks")[0].text)
    except:
        num_range_looks = int(root.findall("./runTopo/inputs/NUMBER_RANGE_LOOKS")[0].text)
    center_range = first_range + (num_range_bin/2-1)*range_pixel_res*num_range_looks
    try:
        incid_angle = float(root.findall("./master/instrument/incidence_angle")[0].text)
    except:
        incid_angle = float(root.findall("./reference/instrument/incidence_angle")[0].text)
    baseline_top = float(root.findall("./baseline/perp_baseline_top")[0].text)
    baseline_bottom = float(root.findall("./baseline/perp_baseline_bottom")[0].text)
    baseline = (baseline_bottom+baseline_top)/2
    try:
        sensor = root.findall("./master/platform/mission")[0].text
    except:
        sensor = root.findall("./reference/platform/mission")[0].text
    
    if sensor == 'ALOS':
        numLooks = 20
    elif sensor == 'ALOS2':
        numLooks = 30
    else:
        raise Exception("invalid sensor: supported sensors include ALOS and ALOS-2 only")

    xmlfilet = [f for f in os.listdir(os.path.join(directory, 'int_'+date1+'_'+date2)) if f.endswith('topophase.cor.geo.xml')][0]
    xmlfile = os.path.join(directory, 'int_'+date1+'_'+date2, xmlfilet)
    #xmlfile = directory+"int_"+date1+"_"+date2+"/topophase.cor.geo.xml"
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
    
    xmlfilet = [f for f in os.listdir(os.path.join(directory, 'int_'+date1+'_'+date2)) if f.endswith('resampOnlyImage.amp.geo.xml')][0]
    xmlfile = os.path.join(directory, 'int_'+date1+'_'+date2, xmlfilet)
    #xmlfile = directory+"int_"+date1+"_"+date2+"/resampOnlyImage.amp.geo.xml"
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    delta_array = np.array([])# Simon Kraatz, UMass Amherst
# April 28, 2020
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
    finnn = os.path.join(directory, "int_" + date1 + "_" + date2, "topophase.cor.geo")
    fid_cor = open(finnn, "rb")
    #fid_cor = open(directory + "int_"+date1+"_"+date2+"/topophase.cor.geo", "rb")
    cor_file = np.fromfile(fid_cor, dtype=np.dtype('<f'))
##    pdb.set_trace()
    corr = cor_file.reshape(2*geo_width, -1, order='F')
    corr = corr[:,0:geo_nlines]
    corr_mag = corr[geo_width:2*geo_width,:]

    finnn = os.path.join(directory, "int_" + date1 + "_" + date2, "resampOnlyImage.amp.geo")
    fid_amp = open(finnn, "rb")
    #fid_amp = open(directory + "int_"+date1+"_"+date2+"/resampOnlyImage.amp.geo", "rb")
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
        if sensor == 'ALOS':
            if root_tag == 'insarProc':
                ####### ALOS thermal noise level (insarApp)
                N1 = 55.5**2
                N2 = 55.5**2
            elif root_tag == 'stripmapProc':
                ####### ALOS thermal noise level (stripmapApp)
                N1 = (55.5/81)**2
                N2 = (55.5/81)**2
            else:
                raise Exception("invalid *Proc.xml file!!!")
        elif sensor == 'ALOS2':
            if root_tag == 'insarProc':
                ####### ALOS-2 thermal noise level (insarApp)
                N1 = 25848**2
                N2 = 25848**2
            elif root_tag == 'stripmapProc':
                ####### ALOS-2 thermal noise level (stripmapApp)
                N1 = 18114**2
                N2 = 18114**2
            else:
                raise Exception("invalid *Proc.xml file!!!")
        else:
            raise Exception("invalid sensor: supported sensors include ALOS and ALOS-2 only")
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
    
    # correct for geocoding shift error
    latshift = mt.fabs(step_lat) * latshift
    longshift = mt.fabs(step_lon) * longshift
    coords = np.array(coords)
    coords[0:2] = coords[0:2] - latshift
    coords[2:4] = coords[2:4] - longshift
    coords = coords.tolist()

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
