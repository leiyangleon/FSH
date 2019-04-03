# cal_KB.py
# Tracy Whelen, Microwave Remote Sensing Lab, University of Massachusetts
# Yang Lei, Microwave Remote Sensing Lab, University of Massachusetts
# November 16, 2015

# This is the python version of cal_KB.m. This function calculates the K and B parameters.

#!/usr/bin/python
from numpy import *
import cal_KB_pairwise_new as kbp
import cal_KB_self_new as kbs
#import time


# define cal_KB function
# input paramters are the dp matrix, number of edges, start scene, an array of all the edge scene pairs, the file directory, 
    # averaging numbers in lat and lon for "self" and "pairwise" fitting, bin_size for density calculation in scatter plot fitting, 
    # flag for sparse data cloud filtering
def cal_KB(dp, edges, start_scene, link, directory, Nd_pairwise, Nd_self, bin_size, flag_sparse):

    # make output matrix of zeros
    YY = zeros((edges + 1) * 2)
    if link.size != 0:
        # for each edge run cal_KB_pairwise_new and put the output into YY
        for i in range(edges):
#            print (time.strftime("%H:%M:%S"))
            k_temp, b_temp = kbp.cal_KB_pairwise_new(int(link[i, 0]), int(link[i, 1]), dp[int((2*link[i, 0])-2)], dp[int((2*link[i, 0])-1)], dp[int((2*link[i, 1])-2)], dp[int((2*link[i, 1])-1)], directory, Nd_pairwise, bin_size)
#            print (time.strftime("%H:%M:%S"))
            YY[2 * i] = k_temp
            YY[(2 * i) + 1] = b_temp

    # run cal_KB_self_new and put output into YY

    k_temp, b_temp = kbs.cal_KB_self_new(dp[int((2 * start_scene) - 2)], dp[int((2 * start_scene) - 1)], directory, Nd_self, bin_size, flag_sparse)
    YY[(2 * (edges + 1)) - 2] = k_temp
    YY[(2 * (edges + 1)) - 1] = b_temp
    
    # return Y
    return YY
