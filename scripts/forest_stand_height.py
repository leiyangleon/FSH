# forest_stand_height.py
# Tracy Whelen, Microwave Remote Sensing Lab, University of Massachusetts
# Yang Lei, Microwave Remote Sensing Lab, University of Massachusetts
# December 8, 2015
# Yang Lei, Jet Propulsion Labortary, California Institute of Technology
# May 18, 2017

# This script calls all the processing steps needed to take ROI_PAC/ISCE output and create a map of tree heights.

#!/usr/bin/python
from numpy import *
import auto_tree_height_many as athm
import read_linkfile as rlnk
import intermediate as inter
import intermediate_self as ins
import auto_mosaicking_new as amn
import write_deltaSC as wSC
import write_mapfile_new as wmn
import write_diff_height_map as wdm
import time
import pdb
import cal_error_metric as cem
import json
import argparse
import commands

# Define forest_stand_height function
# Input parameters are scenes, edges, start scene, iterations, link file, flag file, reference data file, file directory,
# list of all output tree height map file types, averaging numbers in lat and lon for "self" and "pairwise" fitting,
# averaging numbers in lat and lon for "self" and "pairwise" error calculation, bin_size for density calculation in scatter plot fitting,
# flag for sparse data cloud filtering, flag for exporting the diff_height maps, flag for exporting the json error metric files (for all flags 0 is no output, 1 is output)
# number of looks, thermal noise level, flag for processor selection, flag for temporal change gradient correction

def forest_stand_height(scenes, edges, start_scene, iterations, linkfilename, flagfile, ref_file, maskfile, file_directory, filetypes=['gif', 'json', 'kml', 'mat', 'tif'], Nd_pairwise=20, Nd_self=20, N_pairwise=20, N_self=20, bin_size=100, flag_sparse=0, flag_diff=0, flag_error=0, numLooks=20, noiselevel=0.0, flag_proc=0, flag_grad=0):
    
    print (time.strftime("%H:%M:%S"))
    
    # Set error warnings to ignore "invalid value" warnings caused by NaN values
    seterr(invalid='ignore')
    
    if flag_sparse == 1:
        Nd_self = 1

    commands.getoutput('mkdir '+file_directory+'output')
    
    # Extract the correlation map, kz, and corner coordinates for each scene
    athm.auto_tree_height_many(scenes, flagfile, file_directory, numLooks, noiselevel, flag_proc, flag_grad)

    if linkfilename == '-':
        # Run intermediate_self() (Central scene and LiDAR overlap)
        ins.intermediate_self(start_scene, flagfile, ref_file, maskfile, file_directory)
        edge_array = array([])
        print (time.strftime("%H:%M:%S"))
    else:
        # Read in the list of edges
        edge_array = rlnk.read_linkfile(edges, linkfilename, file_directory)
        # Calculate the overlap areas between the different scenes and the LiDAR (or other groundtruth)
        inter.intermediate(edges, start_scene, edge_array, maskfile, flagfile, ref_file, file_directory)

    # Mosaic the interferograms
    amn.auto_mosaicking_new(scenes, edges, start_scene, iterations, edge_array, file_directory, Nd_pairwise, Nd_self, bin_size, flag_sparse)
    
    # Store the delta S and C values for each scene
    wSC.write_deltaSC(scenes, iterations, flagfile, file_directory)
    
    # Create the tree height map
    wmn.write_mapfile_new(scenes, flagfile, maskfile, file_directory, filetypes)
    
    if flag_diff == 1:
        # Create the diff_height map
        wdm.write_diff_height_map(start_scene, ref_file, flagfile, maskfile, file_directory, filetypes)
    
    
    # Run cal_error_metric() when error metrics/scatter plots are needed
    if flag_error == 1:
        # Load the dp vector from the final iteration
        filename = "SC_%d_iter.json" % iterations
        ##        filename = "SC_%d_iter.json" % 6
        iter_file = open(file_directory + "output/" + filename)
        file_data = json.load(iter_file)
        iter_file.close()
        dp = array(file_data[0])
        # Run cal_error_metric() and create a json file containing all of the "pairwise" and "self" R & RMSE error measures
        Y = cem.cal_error_metric(dp, edges, start_scene, edge_array, file_directory, N_pairwise, N_self)
        output_file = open(file_directory + "output/" + "error_metric.json", 'w')
        json.dump([Y.tolist()], output_file)
        output_file.close()
        print "cal_error_metric file written at " + (time.strftime("%H:%M:%S"))

# Gather parameters from the command line and run the function
parser = argparse.ArgumentParser(description="Run Forest Stand Height module")
parser.add_argument('scenes', type=int, help='number of scenes')
parser.add_argument('edges', type=int, help='number of edges')
parser.add_argument('start_scene', type=int, help='flag value of the start scene')
parser.add_argument('iterations', type=int, help='number of iterations')
parser.add_argument('linkfilename', type=str, help='filename of the linkfile')
parser.add_argument('flagfile', type=str, help='filename of the flagfile')
parser.add_argument('ref_file', type=str, help='filename of the reference data file')
parser.add_argument('maskfile', type=str, help='filename of the mask file')
parser.add_argument('file_directory', type=str, help='path of the file directory, make sure to finish with a slash to separate final directory and file')
parser.add_argument('filetypes', type=str, help='string of output file types. File types available: .gif, .json, .kml, .mat, .tif -- input without the ., such as \"kml\" instead of \".kml\"')
parser.add_argument('--Nd_pairwise', type=int, help='pixel-averaging parameter for edge fitting', nargs='?', default=20)
parser.add_argument('--Nd_self', type=int, help='pixel-averaging parameter for central scene fitting', nargs='?', default=10)
parser.add_argument('--N_pairwise', type=int, help='pixel-averaging parameter for edge error metrics', nargs='?', default=20)
parser.add_argument('--N_self', type=int, help='pixel-averaging parameter for central scene error metrics', nargs='?', default=10)
parser.add_argument('--bin_size', type=int, help='bin size for density calculation in sparse data cloud fitting', nargs='?', default=100)
parser.add_argument('--flag_sparse', type=int, help='optional flag for sparse data cloud filtering', choices=[0, 1], nargs='?', default=0)
parser.add_argument('--flag_diff', type=int, help='optional flag for exporting differential height maps', choices=[0, 1], nargs='?', default=0)
parser.add_argument('--flag_error', type=int, help='optional flag for exporting .json error metric files', choices=[0, 1], nargs='?', default=0)
parser.add_argument('--numLooks', type=int, help='number of looks in the correlation estimation', nargs='?', default=20)
parser.add_argument('--noiselevel', type=float, help='sensor thermal noise level (ALOS value hardcoded as default if no value provided)', nargs='?', default=0.0)
parser.add_argument('--flag_proc', type=int, help='optional flag for InSAR processor selection', choices=[0, 1], nargs='?', default=0)
parser.add_argument('--flag_grad', type=int, help='optional flag for correction of large-scale temporal change gradient', choices=[0, 1], nargs='?', default=0)

args = parser.parse_args()

print "\n"
print args
print "\n"

forest_stand_height(args.scenes, args.edges, args.start_scene, args.iterations, args.linkfilename, args.flagfile, args.ref_file, args.maskfile, args.file_directory, args.filetypes.strip().split(" "), args.Nd_pairwise, args.Nd_self, args.N_pairwise, args.N_self, args.bin_size, args.flag_sparse, args.flag_diff, args.flag_error, args.numLooks, args.noiselevel, args.flag_proc, args.flag_grad)
