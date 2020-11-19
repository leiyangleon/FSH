#!/usr/bin/env python3

########
#Yang Lei, Jet Propulsion Laboratory
#November 2017

import xml.etree.ElementTree as ET
from numpy import *
import scipy.io as sio
#import commands
import subprocess
import os
import time
import argparse
import pdb
import os
import isce
import shelve
import string
import sys

def cmdLineParse():
    '''
    Command line parser.
    '''
    parser = argparse.ArgumentParser(description="Single-pair InSAR processing of ALOS data using ISCE modules")
    
    parser.add_argument('-f', '--foldername', dest='foldername', type=str, required=True,
                        help='Folder of the pair of ALOS image data')

    return parser.parse_args()


def runCmd(cmd):
    out = subprocess.getoutput(cmd)
    return out



if __name__ == '__main__':
    
        inps = cmdLineParse()
        
        print (time.strftime("%H:%M:%S"))

        ##########################      Preprocessing      ######################
        
        
        date_array = array([])
        os.chdir(inps.foldername)
        
        try:
            filepath = str.split(runCmd('find `pwd` -name "summary.txt"'))
            sensor = 'ALOS2'
        except:
            filepath = str.split(runCmd('find `pwd` -name "workreport"'))
            sensor = 'ALOS'
        i = 0
        for path in filepath:
            if sensor == 'ALOS2':
                line = runCmd('fgrep Lbi_ObservationDate '+path)
                name = path[0:-12]
                date = line[-9:-1]
            elif sensor == 'ALOS':
                line = runCmd('fgrep Img_SceneCenterDateTime '+path)
                name = path[0:-11]
                date = str.split(line)[2][1:]
            else:
                raise Exception('Unknown sensor; Supported sensors include ALOS and ALOS-2 only')
#            pdb.set_trace()
            date_array = append(date_array, date)
            imagepath = str.split(runCmd('find '+name+' -name "IMG-HV*"'))[0]
            leadpath = str.split(runCmd('find '+name+' -name "LED*"'))[0]
            outpath = date
            component = ET.Element("component")
            IMG = ET.SubElement(component, "property", name="IMAGEFILE")
            ET.SubElement(IMG, "value").text = imagepath
            LED = ET.SubElement(component, "property", name="LEADERFILE")
            ET.SubElement(LED, "value").text = leadpath
            OUT = ET.SubElement(component, "property", name="OUTPUT")
            ET.SubElement(OUT, "value").text = outpath
            tree = ET.ElementTree(component)
#            pdb.set_trace()
            if i == 0:
                tree.write("master.xml")
            else:
                tree.write("slave.xml")
            i = i + 1
        
        if float(date_array[0]) > float(date_array[1]):
            runCmd("mv master.xml temp.xml")
            runCmd("mv slave.xml master.xml")
            runCmd("mv temp.xml slave.xml")
        
        
        print("Preprocessing Done!")
        print (time.strftime("%H:%M:%S"))
        
        ##########################      topsApp.xml generation      ######################

        cmd = 'format_stripmapApp_xml.py -s {0} | tee stripmapAppxml.txt'.format(sensor)
        
        runCmd(cmd)
        
        print("stripmapApp xml Done!")
        print (time.strftime("%H:%M:%S"))
        
        ##########################      ISCE topsApp run      ######################
        
        cmd = 'stripmapApp.py stripmapApp.xml --end=interferogram | tee stripmapApp1.txt'
        
        runCmd(cmd)

        cmd = 'stripmapApp.py stripmapApp.xml --start=interferogram | tee stripmapApp2.txt'
            
        runCmd(cmd)
        
        cmd = 'imageMath.py -e="a_0;a_1" --a ./interferogram/resampOnlyImage1.amp.geo -o ./interferogram/resampOnlyImage.amp.geo -s BIP -t FLOAT'

        runCmd(cmd)

        print("stripmapApp Done!")
        print (time.strftime("%H:%M:%S"))
        


        print("Single pair of ###" + inps.foldername + "### Done !!!")

        print(time.strftime("%H:%M:%S"))
        
        print("\n")

        os.chdir('..')

        

