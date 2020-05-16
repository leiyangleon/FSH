# write_deltaSC.py
# Tracy Whelen, Microwave Remote Sensing Lab, University of Massachusetts
# December 8, 2015
# Simon Kraatz, UMass Amherst
# April 28, 2020

# This script is the python version of write_deltaSC.m, which stores the delta S and C values for each scene.
#!/usr/bin/python

from numpy import *
import json
import time
import flag_scene_file as fsf
import argparse
import os

# Define write_deltaSC function
# Input parameters are the number of scenes, number of iterations, flag-scene name list, and file directory
def write_deltaSC(scenes, N, flagfile, directory):

    # Load dp data from final iteration .json file
    filename = "SC_%d_iter.json" % N
##    filename = "SC_%d_iter.json" % 6
    selffile = open(os.path.join(directory, "output", filename))
    selffile_data = json.load(selffile)
    dp = array(selffile_data[0])

    # For each scene name the file, create delta S and C, and save them to the file
    for i in range(scenes):

        # Set file name
        scene_data = fsf.flag_scene_file(flagfile, i + 1, directory) # 0 vs 1 indexing
        filename = scene_data[1]
        image_folder = "f" + scene_data[4] + "_o" + scene_data[5] + "/"

        # Calculate delta S and C
        DS = dp[2 * i]
        DC = dp[(2 * i) + 1]

        # Save DS and DC to output .json file
        outfile = open(os.path.join(directory, image_folder, filename + '_tempD.json'), "w")
        json.dump([DS, DC], outfile)
        outfile.close()

    print ("write_deltaSC completed at " + (time.strftime("%H:%M:%S")))



# If function is run on its own, gather parameters from the command line and run the function
def main():
    # Gather parameters from the command line and run the function
    parser = argparse.ArgumentParser(description="Run Forest Stand Height module")
    parser.add_argument('scenes', type=int, help='number of scenes')
    parser.add_argument('iterations', type=int, help='number of iterations')
    parser.add_argument('flagfile', type=str, help='filename of the flagfile')
    parser.add_argument('file_directory', type=str, help='path of the file directory, make sure to finish with a slash to separate final directory and file')

    args = parser.parse_args()

    write_deltaSC(args.scenes, args.iterations, args.flagfile, args.file_directory)


if __name__ == "__main__":
    main()
