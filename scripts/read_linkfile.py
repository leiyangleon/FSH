# read_linkfile.py
# Tracy Whelen, Microwave Remote Sensing Lab, University of Massachusetts
# September 30, 2015

# This script reads in a text file containing a list of all the scene pairs and returns a 2-D array with all the pairs

#!/usr/bin/python
from numpy import *
import argparse

# Define read_linkfile function
# Input parameters are the numbers of edges and the name of the file with the edge scene pairs (aka the linkfile)
def read_linkfile(edges, filename, directory):
    if edges > 0:
        # Open the file
        linkfile = open(directory + filename)
    
        # Create output array
        linkarray = zeros(edges * 2).reshape(edges, 2)
    
        # Set line counter
        counter = 0
    
        # For each line in the file compare the line flag with the input flag
        for line in linkfile:
        
            # Set array values from each line
            line = line.strip().split()
            linkarray[counter][0] = line[0]
            linkarray[counter][1] = line[1]
        
            # Increment counter
            counter += 1
            
        # Close file
        linkfile.close()
        
        # Return linkarray
        return linkarray
    else:
        linkarray = []

# If function is run on its own, gather parameters from the command line and run the function  
def main():
    # Gather parameters from the command line and run the function   
    parser = argparse.ArgumentParser(description="Run Forest Stand Height module")
    parser.add_argument('edges', type=int, help='number of edges')
    parser.add_argument('linkfilename', type=str, help='filename of the linkfile')
    parser.add_argument('file_directory', type=str, help='path of the file directory, make sure to finish with a slash to separate final directory and file')

    args = parser.parse_args()
    
    read_linkfile(args.edges, args.linkfilename, args.file_directory)


    
if __name__ == "__main__":
    main()