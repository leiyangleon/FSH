# write_mapfile_new.py
# Tracy Whelen, Microwave Remote Sensing Lab, University of Massachusetts
# December 8, 2015
# Yang Lei, Jet Propulsion Labortary, California Institute of Technology
# May 18, 2017


# This script is the python version of write_mapfile_new.m, which calculates and writes the tree height map to a file.
#!/usr/bin/python

from numpy import *
import json
import time
import argparse
import flag_scene_file as fsf
import arc_sinc as arc
import remove_nonforest as rnf
import write_file_type as wft
import scipy.io as sio
import pdb


# Define write_mapfile_new function
# Input parameters are the number of scenes, flag-scene name list, non-forest maskfile, file directory, and list of output file types
def write_mapfile_new(scenes, flagfile, maskfile, directory, output_files):

    # For each scene
    for i in range(scenes):

        # Set the filename
        scene_data = fsf.flag_scene_file(flagfile, i + 1, directory) # 0 vs 1 indexing
        filename = scene_data[1]
        image_folder = "f" + scene_data[4] + "_o" + scene_data[5] + "/"

        # Load first image file and associated parameters

        file1 = sio.loadmat(directory + image_folder + filename + "_orig.mat")
        corr_vs = file1['corr_vs']
        coords = file1['coords'][0]

#        file1 = open(directory + image_folder + filename + "_orig.json")
#        file1_data = json.load(file1)
#        file1.close()
#
#        # Set parameter values based on file1_data
#        corr_vs = array(file1_data[0])
#        coords = array(file1_data[2])

        # Load and read data from temp .json files
        file_tempD = open(directory + image_folder + filename + "_tempD.json")
        B = json.load(file_tempD)

        # Set S and C paramters based on the default and data from B
        S_param = 0.65 + B[0]
        C_param = 13 + B[1]

        # Run interpolation to calculate the heights
        gamma = corr_vs.copy()
        gamma = gamma / S_param
        height = arc.arc_sinc(gamma, C_param)
        height[isnan(gamma)] = nan

        # Mask out non-forest areas
        if maskfile != '-':
            forest_only_height = rnf.remove_nonforest(height, coords, maskfile, directory)
        else:
            forest_only_height = height

        # Transpose height to correctly align it (ie so it isn't rotated in relation to an underlying map)
        forest_only_height = forest_only_height.transpose()

        # Get rid of NaN so future processing software doesn't error
#        forest_only_height = forest_only_height + 0.000001
        forest_only_height[isnan(forest_only_height)] = 255

        #pdb.set_trace()

        # Write all the desired output file types for the forest height map
        for filetype in output_files:
            wft.write_file_type(forest_only_height, "stand_height", filename, directory + image_folder, filetype, coords)

    print ("all tree height map files written at "+ (time.strftime("%H:%M:%S")))


# If function is run on its own, gather parameters from the command line and run the function
def main():
    # Gather parameters from the command line and run the function
    parser = argparse.ArgumentParser(description="Run Forest Stand Height module")
    parser.add_argument('scenes', type=int, help='number of scenes')
    parser.add_argument('flagfile', type=str, help='filename of the flagfile')
    parser.add_argument('maskfile', type=str, help='filename of the mask file')
    parser.add_argument('file_directory', type=str, help='path of the file directory, make sure to finish with a slash to separate final directory and file')
    parser.add_argument('output_files', type=str, help='string of output file types. File types available: .gif, .json, .kml, .mat, .tif -- input without the ., such as \"kml\" instead of \".kml\"')

    args = parser.parse_args()

    write_mapfile_new(args.scenes, args.flagfile, args.maskfile, args.file_directory, args.output_files.strip().split(" "))



if __name__ == "__main__":
    main()
