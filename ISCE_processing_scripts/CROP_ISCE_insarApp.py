#!/usr/bin/env python3


# Yang Lei, Jet Propulsion Laboratory
# September, 2016

# This script crops the ISCE output files in radar coordinates by eliminating the erroneous edge effects.

#!/usr/bin/python
import numpy as np
#import read_rsc_data as rrd
import sys
import pdb
import xml.etree.ElementTree as ET
import argparse
import subprocess
import logging
from imageMath import IML
import time



def cmdLineParse():
    '''
        Command line parser.
        '''
    parser = argparse.ArgumentParser(description="Single-pair InSAR processing of ALOS data using ISCE modules")
    parser.add_argument('-a', '--ampname', dest='ampname', type=str, required=True,
                help='amp filename')
    parser.add_argument('-c', '--corname', dest='corname', type=str, required=True,
                help='cor filename')
    
    
    
    return parser.parse_args()


def runCmd(cmd):
    out = subprocess.getoutput(cmd)
    return out


if __name__ == '__main__':
    
    inps = cmdLineParse()
    
    print('################################################')
    print ('Crop Start!!!')
    print (time.strftime("%H:%M:%S"))


    
    nanval = 0.0
    
    
    # Read amp files in radar coordinates
#    ampfile = "./interferogram/topophase.amp"
    ampfile = inps.ampname
    inty = IML.mmapFromISCE(ampfile, logging)
    inty1 = inty.bands[0].copy()
    inty2 = inty.bands[1].copy()
#    inty1[inty1==nanval] = np.NaN
#    inty2[inty2==nanval] = np.NaN

    width = inty1.shape[1]
    length = inty1.shape[0]



    # Creating empty array for cropped square list
    
    inty1[:176,:] = nanval
    inty1[5488:,:] = nanval
    inty1[:,:163] = nanval
    inty1[:,4846:] = nanval

    inty2[:176,:] = nanval
    inty2[5488:,:] = nanval
    inty2[:,:163] = nanval
    inty2[:,4846:] = nanval


    # Write amp files
    mliImage = np.ones((length,2*width))
    mliImage[:,::2] = inty1
    mliImage[:,1::2] = inty2
    
    mliFid = open(ampfile, 'wb')
    
    for yy in range(length):
        data = mliImage[yy,:]
        data.astype(np.float32).tofile(mliFid)
    
    mliFid.close()
    
#    img = isceobj.createAmpImage()
#    img.setFilename(ampfile)
#    img.setWidth(width)
#    img.setLength(length)
#    img.setAccessMode('READ')
#    img.renderHdr()


    # Read cor files in radar coordinates
#    corfile = "./interferogram/topophase.cor"
    corfile = inps.corname
    inty_corr = IML.mmapFromISCE(corfile, logging)
    inty = inty_corr.bands[0].copy()
    corr = inty_corr.bands[1].copy()
#    inty[inty==nanval] = np.NaN
#    corr[corr==nanval] = np.NaN

    width = inty.shape[1]
    length = inty.shape[0]



    # Creating empty array for cropped square list

    inty[:176,:] = nanval
    inty[5488:,:] = nanval
    inty[:,:163] = nanval
    inty[:,4846:] = nanval

    corr[:176,:] = nanval
    corr[5488:,:] = nanval
    corr[:,:163] = nanval
    corr[:,4846:] = nanval

    # Write cor files
    COR_DATA = np.single(np.ones((length,2*width)))
    COR_DATA[:,0:width] = inty
    COR_DATA[:,width:2*width] = corr

    corFid = open(corfile, 'wb')
    
    for yy in range(length):
        data = COR_DATA[yy,:]
        data.astype(np.float32).tofile(corFid)

    corFid.close()

#    img = isceobj.createBILImage()
#    img.setFilename(corfile)
#    img.setWidth(width)
#    img.setLength(length)
#    img.setAccessMode('READ')
#    img.renderHdr()

    print('Crop Done!!!')
    print (time.strftime("%H:%M:%S"))
    print('################################################')
