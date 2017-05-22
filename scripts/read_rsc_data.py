# read_rsc_data.py
# Gerard Ruiz Carregal, Microwave Remote Sensing Lab, University of Massachusetts
# July 10, 2015

# This script reads the value of the given parameter from the ROI_PAC output rsc file

#!/usr/bin/python

# Define read_rsc_data function
# Input parameters are the filename of the input rsc text file, the file directory, and the name of the desired parameter
def read_rsc_data(filename, directory, param):
    
    # Set default output value
    result = -1
    
    # Set filename for file to be searched
    rsc_file = directory + filename
    
    # Read parameters from file
    for line in open(rsc_file):
        if line.startswith(param):
            result = float(line.strip().split()[1])

    return result