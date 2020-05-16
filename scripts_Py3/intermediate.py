# intermediate.py
# Tracy Whelen, Microwave Remote Sensing Lab, University of Massachusetts
# November 16, 2015
# Yang Lei, Jet Propulsion Labortary, California Institute of Technology
# May 18, 2017
# Simon Kraatz, UMass Amherst
# April 28, 2020

# This script is the python version of intermediate.m, which calculates the overlap areas, running intermediate_self
# and intermediate_pairwise for each each edge.

#!/usr/bin/python

from numpy import *
import time
import intermediate_pairwise as inp
import intermediate_self as ins
import argparse
import os


# Define intermediate function
# Input parameters are the number of edges, central scene flag number, the array of edge scene pairs, the non-forest mask, flag-scene name list, reference data file, and the file directory
def intermediate(edges, start_scene, linkarray, maskfile, flagfile, ref_file, directory):
    # For each edge run intermediate_pairwise
    for i in range(edges):
        inp.intermediate_pairwise(linkarray[i, 0], linkarray[i, 1], flagfile, maskfile, directory)
        print (("%d edge file(s) created at " % (i + 1)) + (time.strftime("%H:%M:%S")))
        
    # Run intermediate_self() (Central scene and LiDAR overlap)
    ins.intermediate_self(start_scene, flagfile, ref_file, maskfile, directory)
    
    print ("intermediate() complete - overlap areas calculated at " + (time.strftime("%H:%M:%S")))
    
    
# If function is run on its own, gather parameters from the command line and run the function  
def main(): 
    # Gather parameters from the command line and run the function   
    parser = argparse.ArgumentParser(description="Run Forest Stand Height module")
    parser.add_argument('edges', type=int, help='number of edges')
    parser.add_argument('start_scene', type=int, help='flag value of the start scene')
    parser.add_argument('linkfilename', type=str, help='filename of the linkfile')
    parser.add_argument('maskfile', type=str, help='filename of the mask file')
    parser.add_argument('flagfile', type=str, help='filename of the flagfile')
    parser.add_argument('ref_file', type=str, help='filename of the reference data file')
    parser.add_argument('file_directory', type=str, help='path of the file directory, make sure to finish with a slash to separate final directory and file')
    
    args = parser.parse_args()    
    
    # Create the linkarray from the linkfile name, rather than trying to pass a 2D array into the command line
    linkarray = rlf.read_linkfile(args.edges, args.linkfilename, args.file_directory)
    
    intermediate(args.edges, args.start_scene, linkarray, args.maskfile, args.flagfile, args.ref_file, args.file_directory)    

    
if __name__ == "__main__":
    main()
