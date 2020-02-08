# remove_outlier.py
# Tracy Whelen, Microwave Remote Sensing Lab, University of Massachusetts
# May 28, 2015

# This is the python version of remote_outlier.m.

#!/usr/bin/python
from numpy import *

# define remove_outlier function
# input parameters are column vector each of x and y points (together they are a list of points),
# a window size for searching for neighboring points, and a threshold that defines whether or not
# there are few enough neighboring points to be considered an outlier.
# win_size and threshold are optional parameters with defaults of 0.5 and 5 respectively
def remove_outlier(x, y, win_size=0.5, threshold=5):

    # initialize other variables
    outliers_ind = [] # in Matlab code this variable is IND
    ind_x = zeros(x.size)
    ind_y = zeros(x.size)
    ind = zeros(x.size)

    # For each value in x check more or less neighboring points within the given window than the given threshold
    for i in range(x.size):

        # set base equal to a pair of x, y values        
        current_x = x[i]
        current_y = y[i]

        # for each x and y check if they are within +- the window from the current x(i) and y(i)
        # store a list of where both a and y are within the window in the array ind
        ind_x = (x > current_x - win_size) & (x < current_x + win_size) 
        ind_y = (y > current_y - win_size) & (y < current_y + win_size)
        ind = ind_x & ind_y

        # if for the current i there are fewer nearby points (within window) than the threshold
        if sum(ind) <= threshold:
            # then append it to the outliers array
            outliers_ind.append(i)

    # make new copies of x and y and delete all of the outlying points
    XX = delete(x, outliers_ind)
    YY = delete(y, outliers_ind)

    # return XX and YY    (aka x and y without the outliers)
    return XX, YY