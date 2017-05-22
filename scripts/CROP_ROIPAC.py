# CROP_ROIPAC.py
# Diya Chowdhury, Applied GeoSolutions
# Yang Lei, Microwave Remote Sensing Lab, University of Massachusetts
# October 12, 2015

# This script crops the ROI_PAC output files in radar coordinates by eliminating the erroneous edge effects.

#!/usr/bin/python
import numpy as np
import read_rsc_data as rrd
import sys
import pdb

directory = sys.argv[1]					# Directory where amp/cor files are
date1 = sys.argv[2]						# SAR date1
date2 = sys.argv[3]						# SAR date2

# Extract ROI_PAC parameters
amp_rsc_file = date1+"-"+date2+"_2rlks.amp.rsc"
width = int(rrd.read_rsc_data(amp_rsc_file, directory, "WIDTH"))
length = int(rrd.read_rsc_data(amp_rsc_file, directory, "FILE_LENGTH"))
fullwidth = width*2
nanval = 0

# Read cor files in radar coordinates
cor_file = np.fromfile(directory+date1+"-"+date2+"_2rlks.cor",dtype='f4', count=length*fullwidth)
corr = cor_file.reshape((length, fullwidth))
mag = corr[:,0:width]
phs = corr[:,width:fullwidth]

# Read amp files in radar coordinates
amp_file = np.fromfile(directory+date1+"-"+date2+"_2rlks.amp", dtype='complex64')
inty = amp_file.reshape((length,width))

# Creating empty array for cropped square list
mag[:638,:] = nanval
mag[3288:,:] = nanval
mag[:,:84] = nanval
mag[:,2418:] = nanval

phs[:638,:] = nanval
phs[3288:,:] = nanval
phs[:,:84] = nanval
phs[:,2418:] = nanval

inty[:638,:] = nanval
inty[3288:,:] = nanval
inty[:,:84] = nanval
inty[:,2418:] = nanval

# Creating empty array for square list
c_out = np.zeros((length,fullwidth))

# Writing vals
c_out[:,0:width] = mag
c_out[:,width:fullwidth] = phs

# Write output files
cx = c_out.astype('f4')
cx.tofile(directory + date1+"-"+date2+"_2rlks_fix.cor")
inty.tofile(directory + date1+"-"+date2+"_2rlks_fix.amp")
