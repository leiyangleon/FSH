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
from scipy import signal
import argparse
import subprocess
import logging
from imageMath import IML
import cv2
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
    print ('Multilook Start!!!')
    print (time.strftime("%H:%M:%S"))
    

    nanval = 0.0
    
    # Read amp files in radar coordinates
#    ampfile = "./interferogram/topophase.amp"
    ampfile = inps.ampname
    inty = IML.mmapFromISCE(ampfile, logging)
    inty1 = inty.bands[0].copy()
    inty2 = inty.bands[1].copy()
    inty1[inty1==nanval] = np.NaN
    inty2[inty2==nanval] = np.NaN
    
    width = inty1.shape[1]
    length = inty1.shape[0]




    # multi-look filtering amp file
    inty1 = np.power(inty1,2);
    inty2 = np.power(inty2,2);
    mask = np.ones((2,2))
    INTY1 = cv2.filter2D(inty1, -1, mask, borderType=cv2.BORDER_CONSTANT)/np.sum(mask)
#    INTY1 = signal.convolve2d(inty1, mask, boundary='symm', mode='same')/mask.size
    INTY2 = cv2.filter2D(inty2, -1, mask, borderType=cv2.BORDER_CONSTANT)/np.sum(mask)
#    INTY2 = signal.convolve2d(inty2, mask, boundary='symm', mode='same')/mask.size
    INTY1 = np.sqrt(INTY1)
    INTY2 = np.sqrt(INTY2)
#    pdb.set_trace()
    INTY1[np.isnan(INTY1)] = nanval
    INTY2[np.isnan(INTY2)] = nanval
    
    # Write amp files
    mliImage = np.ones((length,2*width))
    mliImage[:,::2] = INTY1
    mliImage[:,1::2] = INTY2
    
    
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
    inty[inty==nanval] = np.NaN
    corr[corr==nanval] = np.NaN

    width = inty.shape[1]
    length = inty.shape[0]




    # multi-look filtering cor file
    inty = np.power(inty,2);
    INTY = cv2.filter2D(inty, -1, mask, borderType=cv2.BORDER_CONSTANT)/np.sum(mask)
#    INTY = signal.convolve2d(inty, mask, boundary='symm', mode='same')/mask.size
    CORR = cv2.filter2D(corr, -1, mask, borderType=cv2.BORDER_CONSTANT)/np.sum(mask)
#    CORR = signal.convolve2d(corr, mask, boundary='symm', mode='same')/mask.size
    INTY = np.sqrt(INTY)
    INTY[np.isnan(INTY)] = nanval
    CORR[np.isnan(CORR)] = nanval


    # Write cor files
    COR_DATA = np.single(np.ones((length,2*width)))
    COR_DATA[:,0:width] = INTY
    COR_DATA[:,width:2*width] = CORR
    
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

    print ('Multilook Done!!!')
    print (time.strftime("%H:%M:%S"))
    print('################################################')
