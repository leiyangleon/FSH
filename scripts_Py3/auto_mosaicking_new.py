# auto_mosaicking_new.py
# Tracy Whelen, Microwave Remote Sensing Lab, University of Massachusetts
# Yang Lei, Microwave Remote Sensing Lab, University of Massachusetts
# December 8, 2015
# Simon Kraatz, UMass Amherst
# April 28, 2020

# This is the python version of auto_mosaicking_new.m, which automatically calculates all the S and C paramters
# in preparation for forest height estimation.

# import statements
#!/usr/bin/python
from numpy import *
import time
import json
import cal_KB as cKB
import ls_deltaSC as lSC
import read_linkfile as rlf
import argparse
import time
import pdb
import os

# Define auto_mosaicking_new function
# Input parameters are the numbers of scenes, edges, start scene, iterations, the input/output file directory, 
    # averaging numbers in lat and lon for "self" and "pairwise" fitting, bin_size for density calculation in scatter plot fitting, 
    # flag for sparse data cloud filtering.
def auto_mosaicking_new(scenes, edges, start_scene, N, linkarray, directory, Nd_pairwise, Nd_self, bin_size, flag_sparse):

#    pdb.set_trace()

    # Set average S and C parameters (0<s<1, 0<c<20 so s=0.65 and c=13)
    avg_S = 0.65
    avg_C = 13
    
    # Create avg_dp matrix, and fill  with average S and C parameters
    avg_dp = zeros(scenes * 2)
    put(avg_dp, range(0, scenes * 2, 2), avg_S)
    put(avg_dp, range(1, scenes * 2, 2), avg_C)
    
    # Create the dp matrix 
    # the difference of the avg and the initial SC values OR all zeros (avg - avg)
    dp = zeros(scenes * 2)

    # Initialize target matrix and fill with K=1, B=0
    target_KB = zeros((edges + 1) * 2)
    put(target_KB, range(0, (edges + 1) * 2, 2), 1)

    # Run cal_KB()
    Y = cKB.cal_KB(dp, edges, start_scene, linkarray, directory, Nd_pairwise, Nd_self, bin_size, flag_sparse)

    # Calculate the residual for cal_KB - target
    res = sum((Y - target_KB)**2)



    # Save dp and the residual as the first iteration output file (using JSON)
    iter_file = open(os.path.join(directory, "output", "SC_0_iter.json"), 'w')
    json.dump([dp.tolist(), res], iter_file)
    iter_file.close()
    
##    iter_file = open(directory + "output/" + "SC_5_iter.json", 'r')
##    file_data = json.load(iter_file)
##    dp = array(file_data[0])


    # For the rest of the iterations run ls_deltaSC() and save to output file (using JSON)
    for i in range(1, N + 1, 1): # this will run from i=1 to i=N
        [dp, res] = lSC.ls_deltaSC(dp, edges, scenes, start_scene, linkarray, directory, Nd_pairwise, Nd_self, bin_size, flag_sparse)
        print ("%d iterations completed!\n" % i)
        print (time.strftime("%H:%M:%S"))
        filename = "SC_%d_iter.json" % i
##        filename = "SC_%d_iter.json" % (i+5)
        iter_file = open(os.path.join(directory, "output", filename), 'w')
        json.dump([dp.tolist(), res], iter_file)
        iter_file.close()

    print ("auto_mosaicking_new finished at " + (time.strftime("%H:%M:%S")))



# If function is run on its own, gather parameters from the command line and run the function  
def main():   
    # Gather parameters from the command line and run the function   
    parser = argparse.ArgumentParser(description="Run auto_mosaicking_new script")    
    parser.add_argument('scenes', type=int, help='number of scenes')
    parser.add_argument('edges', type=int, help='number of edges')
    parser.add_argument('start_scene', type=int, help='flag value of the start scene')
    parser.add_argument('iterations', type=int, help='number of iterations')
    parser.add_argument('linkfilename', type=str, help='filename of the linkfile')
    parser.add_argument('file_directory', type=str, help='path of the file directory, make sure to finish with a slash to separate final directory and file')
    parser.add_argument('--Nd_pairwise', type=int, help='pixel-averaging parameter for edge fitting', nargs='?', default=20)
    parser.add_argument('--Nd_self', type=int, help='pixel-averaging parameter for central scene fitting', nargs='?', default=10)
    parser.add_argument('--bin_size', type=int, help='bin size for density calculation in sparse data cloud fitting', nargs='?', default=100)
    parser.add_argument('--flag_sparse', type=int, help='optional flag for sparse data cloud filtering', choices=[0, 1], nargs='?', default=0)

    
    args = parser.parse_args()
    
    # Create the linkarray from the linkfile name, rather than trying to pass a 2D array into the command line
    linkarray = rlf.read_linkfile(args.edges, args.linkfilename, args.file_directory)
    
    auto_mosaicking_new(args.scenes, args.edges, args.start_scene, args.iterations, linkarray, args.file_directory, args.Nd_pairwise, args.Nd_self, args.bin_size, args.flag_sparse)

if __name__ == "__main__":
    main()
