# mean_wo_nan.py
# Tracy Whelen, Microwave Remote Sensing Lab, University of Massachusetts
# May 4, 2015

# This is the python version of mean_wo_nan.m, which calculates and returns the mean of all number values
# in an array (aka all non-NaN values).

#!/usr/bin/python
from numpy import *

# define mean_wo_nan function
# input parameter is an array
def mean_wo_nan(A):

    # Copy and flatten A
    B = A.copy().flatten(1)
    
    # Remove NaN values from B
    B = B[~isnan(B)]
    
    # Return the mean of B
    return mean(B)
