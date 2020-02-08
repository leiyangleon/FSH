# auto_tree_height_many.py
# Tracy Whelen, Microwave Remote Sensing Lab, University of Massachusetts
# December 8, 2015
# Yang Lei, Jet Propulsion Labortary, California Institute of Technology
# May 18, 2017

# This script runs auto_tree_height_single.py for each scene, and saves the output to two files.
# A .mat file stores the correlation map, kz value, and corner coordinates.
# A text file stores the geodata (width, lines, corner lat and lon, and lat and lon step values)

#!/usr/bin/python

from numpy import *
import json
import scipy.io as sio
import time
import argparse
import flag_scene_file as fsf
import auto_tree_height_single_ROIPAC as athsR
import auto_tree_height_single_ISCE as athsI

# Define auto_tree_height_many function
# Input parameters are the central scene, the flag-scene data file, and the file directory, number of looks, noise level, flag for processor selection, flag for correction of temporal change gradient
def auto_tree_height_many(scenes, flagfile, directory, numLooks, noiselevel, flag_proc, flag_grad):

    # For each scene name the file, run auto_tree_height_single and save the output to a .json file
    for i in range(scenes):

        # Get the scene data and set the file name and image folder name (f#_o# where # is the frame and orbit numbers, respectively)
        scene_data = fsf.flag_scene_file(flagfile, i + 1, directory) # 0 vs 1 indexing
        filename = scene_data[1]
        image_folder = "f" + scene_data[4] + "_o" + scene_data[5] + "/"

        # Run auto_tree_height_single
        if flag_proc == 0:
            ######## ROI_PAC results
            file_data = athsR.auto_tree_height_single_ROIPAC(directory + image_folder, scene_data[2], scene_data[3], numLooks, noiselevel, flag_grad)
        elif flag_proc == 1:
            ######## ISCE results
            file_data = athsI.auto_tree_height_single_ISCE(directory + image_folder, scene_data[2], scene_data[3], numLooks, noiselevel, flag_grad)
        else:
            print ("Invalid processor provided!!!")


        #        sio.savemat(directory + filename + '_orig.mat', {'corr_vs':file_data[0], 'kz':file_data[1], 'coords':file_data[2]})

        # Save correlation map, kz, and corner coordinates to output .json file (respectively first three values in file_data)

        ##        outfile = open(directory + image_folder + filename + '_orig.json', "w")
        ##        json.dump([file_data[0].tolist(), file_data[1], file_data[2]], outfile)
        ##        outfile.close()

        linkfile = directory + image_folder + filename + '_orig.mat'
        sio.savemat(linkfile,{'corr_vs':file_data[0],'kz':file_data[1],'coords':file_data[2]})

        # Write geodata to a text file (4th - 9th values in file_data) -> this gets stored in the scene specific folder
        geofile = open(directory + image_folder + filename + "_geo.txt", "w")
        geofile.write("width: %d \n" % file_data[3])
        geofile.write("nlines: %d \n" % file_data[4])
        geofile.write("corner_lat: %f \n" % file_data[5])
        geofile.write("corner_lon: %f \n" % file_data[6])
        geofile.write("post_lat: %f \n" % file_data[7])
        geofile.write("post_lon: %f \n" % file_data[8])
        geofile.close()

    print ("auto_tree_height_many finished at " + (time.strftime("%H:%M:%S")))


# If function is run on its own, gather parameters from the command line and run the function
def main():
    # Gather parameters from the command line and run the function
    parser = argparse.ArgumentParser(description="Run Forest Stand Height module")
    parser.add_argument('scenes', type=int, help='number of scenes')
    parser.add_argument('flagfile', type=str, help='filename of the flagfile')
    parser.add_argument('file_directory', type=str, help='path of the file directory, make sure to finish with a slash to separate final directory and file')
    parser.add_argument('--numLooks', type=int, help='number of looks in the correlation estimation', nargs='?', default=20)
    parser.add_argument('--noiselevel', type=float, help='sensor thermal noise level (ALOS value hardcoded as default if no value provided)', nargs='?', default=0.0)
    parser.add_argument('--flag_proc', type=int, help='optional flag for InSAR processor selection', choices=[0, 1], nargs='?', default=0)
    parser.add_argument('--flag_grad', type=int, help='optional flag for correction of large-scale temporal change gradient', choices=[0, 1], nargs='?', default=0)


    args = parser.parse_args()

    auto_tree_height_many(args.scenes, args.flagfile, args.file_directory, args.numLooks, args.noiselevel, args.flag_proc, args.flag_grad)


if __name__ == "__main__":
    main()
