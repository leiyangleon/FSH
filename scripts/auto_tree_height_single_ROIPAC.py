# auto_tree_height_single_ROIPAC.py
# Gerard Ruiz Carregal, Microwave Remote Sensing Lab, University of Massachusetts
# Yang Lei, Microwave Remote Sensing Lab, University of Massachusetts
# Tracy Whelen, Microwave Remote Sensing Lab, University of Massachusetts
# December 8, 2015
# Yang Lei, Jet Propulsion Labortary, California Institute of Technology
# May 18, 2017

# This script extracts the correlation values, kz value, corner coordinates, and geodata from the ROI_PAC output files.

#!/usr/bin/python
import numpy as np
import math as mt
import read_rsc_data as rrd
import remove_corr_bias as rcb

# Define auto_tree_height_single function
# Input parameters are the file directory, and the names of the two image files
def auto_tree_height_single_ROIPAC(directory, date1, date2, numLooks, noiselevel, flag_grad):

    # Extract ROI_PAC parameters
    amp_rsc_file = "int_"+date1+"_"+date2+"/"+date1+"-"+date2+".amp.rsc"
    range_pixel_res = rrd.read_rsc_data(amp_rsc_file, directory, "RANGE_PIXEL_SIZE")
    azimuth_pixel_res = rrd.read_rsc_data(amp_rsc_file, directory, "AZIMUTH_PIXEL_SIZE")
#    pixel_area = range_pixel_res * azimuth_pixel_res

    geo_cor_rsc_file = "int_"+date1+"_"+date2+"/"+"geo_"+date1+"-"+date2+"_2rlks.cor.rsc"
    geo_width = int(rrd.read_rsc_data(geo_cor_rsc_file, directory, "WIDTH"))
    geo_nlines = int(rrd.read_rsc_data(geo_cor_rsc_file, directory, "FILE_LENGTH"))
    corner_lat = rrd.read_rsc_data(geo_cor_rsc_file, directory, "Y_FIRST")
    corner_lon = rrd.read_rsc_data(geo_cor_rsc_file, directory, "X_FIRST")
    step_lat = rrd.read_rsc_data(geo_cor_rsc_file, directory, "Y_STEP")
    step_lon = rrd.read_rsc_data(geo_cor_rsc_file, directory, "X_STEP")
    llambda = rrd.read_rsc_data(geo_cor_rsc_file, directory, "WAVELENGTH")

    int_rsc_file = "int_"+date1+"_"+date2+"/"+date1+"-"+date2+"-sim_SIM_2rlks.int.rsc"
    range1 = rrd.read_rsc_data(int_rsc_file, directory, "RGE_REF1")
    range2 = rrd.read_rsc_data(int_rsc_file, directory, "RGE_REF2")
    center_range = (range1 + range2) / 2 * 1000

    amp_4rlks_file = "int_"+date1+"_"+date2+"/"+date1+"-"+date2+"_2rlks.amp.rsc"
    incid_angle = rrd.read_rsc_data(amp_4rlks_file, directory, "BEAM")

    baseline_file = "int_"+date1+"_"+date2+"/"+date1+"_"+date2+"_baseline.rsc"
    p_baseline_1 = rrd.read_rsc_data(baseline_file, directory, "P_BASELINE_BOTTOM_HDR")
    p_baseline_2 = rrd.read_rsc_data(baseline_file, directory, "P_BASELINE_TOP_HDR")
    baseline = (p_baseline_1 + p_baseline_2) / 2

    # Read geolocated amp and cor files
    fid_cor = open(directory + "int_"+date1+"_"+date2+"/geo_"+date1+"-"+date2+"_2rlks.cor", "rb")
    cor_file = np.fromfile(fid_cor, dtype=np.dtype('<f'))
    corr_mag = cor_file.reshape(2*geo_width, geo_nlines, order='F')
    corr_mag = corr_mag[geo_width:len(corr_mag),:]

    fid_amp = open(directory + "int_"+date1+"_"+date2+"/geo_"+date1+"-"+date2+"_2rlks.amp", "rb")
    amp_file = np.fromfile(fid_amp, dtype=np.dtype('<f'))
    inty = amp_file.reshape(2*geo_width, geo_nlines, order='F')
    inty1 = inty[::2,:]
    inty2 = inty[1::2,:]

    # Set coordinate list
    coords = [corner_lat, corner_lat+(geo_nlines-1)*step_lat, corner_lon, corner_lon+(geo_width-1)*step_lon]
    
    # Operations
    inty1 = np.power(inty1,2) / 20                  # Hardcoded based on 2 range looks and 10 azimuth looks
    inty2 = np.power(inty2,2) / 20

    inty1[inty1 <= 0] = np.NaN
    inty2[inty2 <= 0] = np.NaN
    corr_mag[corr_mag <= 0] = np.NaN  

################### Noise level for ROI_PAC-processed SAR backscatter power output
    if noiselevel == 0.0:
        ####### ALOS thermal noise level
        N1 = 0.0192                                     
        N2 = 0.0192
    else:
        N1 = noiselevel
        N2 = noiselevel

    S1 = inty1 - N1
    g_th_1 = np.zeros(S1.shape)
    g_th_1[S1>0] = np.sqrt(S1[S1>0] / (S1[S1>0] + N1))
    g_th_1[np.isnan(S1)] = np.NaN
    g_th_1[S1 <= 0] = np.NaN
    
    S2 = inty2-N2
    g_th_2 = np.zeros(S2.shape)
    g_th_2[S2>0] = np.sqrt(S2[S2>0] / (S2[S2>0] + N2))
    g_th_2[np.isnan(S2)] = np.NaN
    g_th_2[S2 <= 0] = np.NaN
    
    g_th = g_th_1 * g_th_2

    corr_mag[corr_mag<0] = 0
    corr_mag[corr_mag>1] = 1
    corr_mag = rcb.remove_corr_bias(corr_mag,numLooks)
    corr_mag[corr_mag<0] = 0
    
    corr_vs = corr_mag / g_th
    
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
