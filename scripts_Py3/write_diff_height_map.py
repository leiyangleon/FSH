# write_diff_height_map.py
# Yang Lei, Microwave Remote Sensing Lab, University of Massachusetts
# Tracy Whelen, Microwave Remote Sensing Lab, University of Massachusetts
# December 8, 2015
# Yang Lei, Jet Propulsion Labortary, California Institute of Technology
# May 18, 2017
# Simon Kraatz, UMass Amherst
# April 28, 2020

# This script writes the forest diff_height map over the lidar-covered area. The pixelwise value in this map is the absolute differece between the 
# lidar height and the InSAR inverted height. 
#!/usr/bin/python

from numpy import *
from scipy import signal
import json
import time
import sys
import flag_scene_file as fsf
import arc_sinc as arc
#import write_file_type_diff_height as wftd
import write_file_type as wft
import scipy.io as sio
import pdb
import os

# Define write_diff_height_map function
# Input parameters are the start_scene, flag-scene name list, non-forest maskfile, file directory, and list of output file types
def write_diff_height_map(start_scene, ref_file, flagfile, maskfile, directory, output_files):
    
    if isinstance(start_scene,int) == 1:
#        # Load image data file 
#        file = open(directory + "output/" + "self.json")
#        file_data = json.load(file)
#        file.close()
#    
#        # Set lidar and InSAR coherence values based on file_data
#        lidar = array(file_data[0])
#        corr_vs = array(file_data[1])

        # Load and read data from .mat file
        # Samples and lines are calculated from the shape of the images
        file_data = sio.loadmat(os.path.join(directory, "output", "self.mat"))
        lidar = file_data['I1']
        corr_vs = file_data['I2']
        
    
        # Load and read data from temp .json files
        scene_data = fsf.flag_scene_file(flagfile, start_scene, directory) # 0 vs 1 indexing
        filename = scene_data[1]
        image_folder = "f" + scene_data[4] + "_o" + scene_data[5] + "/"
        file_tempD = open(os.path.join(directory, image_folder, filename + "_tempD.json"))
        B = json.load(file_tempD)
        
        # Set S and C paramters based on the default and data from B
        S_param = 0.65 + B[0]
        C_param = 13 + B[1]
        
        # Run sinc model to calculate the heights
        gamma = corr_vs.copy()
        gamma = gamma / S_param
        height = arc.arc_sinc(gamma, C_param)
        
        # Calculate the diff_height map (diviation of the InSAR inverted height away from the lidar height)
        diff_height = lidar - height
        
        # Transpose height to correctly align it (ie so it isn't rotated in relation to an underlying map)
        diff_height = diff_height.transpose()
        
        # Get rid of NaN so future processing software doesn't error
##        diff_height = diff_height + spacing(1)
        diff_height[isnan(diff_height)] = 255
        
##        # Low-pass filter to remove the noisy features
##        window = ones([7,7])
##        filt_diff_height = signal.convolve2d(diff_height, window, mode='same') / window.size

        # Write all the desired output file types for the forest diff_height map
#        filename = filename + "_DIST" -> this is taken care of in write_file_type
        for filetype in output_files:
#            wftd.write_file_type_diff_height(diff_height, ref_file, filename, directory, filetype)
            wft.write_file_type(diff_height, "diff_height", filename, os.path.join(directory, image_folder), filetype, 0, ref_file)
            
    print ("all diff_height output files written at " + (time.strftime("%H:%M:%S")))
    
    
# If function is run on its own, gather parameters from the command line and run the function  
def main():
    start_scene = sys.argv[1]
    ref_file = sys.argv[2]
    flagfile = sys.argv[3]
    maskfile = sys.argv[4]
    directory = sys.argv[5]
    output_files = sys.argv[6]
    
    write_diff_height_map(start_scene, ref_file, flagfile, maskfile, directory, output_files)
    
    
if __name__ == "__main__":
    main()
