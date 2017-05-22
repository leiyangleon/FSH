# cal_error_metric.py
# Yang Lei, Microwave Remote Sensing Lab, University of Massachusetts
# Tracy Whelen, Microwave Remote Sensing Lab, University of Massachusetts
# November 16, 2015

# This function calculates the R and RMSE error metrics.

#!/usr/bin/python
from numpy import *
import cal_error_metric_pairwise as emp
import cal_error_metric_self as ems
import pdb

# define cal_error_metric function
# input paramters are the dp matrix, number of edges, start scene, an array of all the edge scene pairs, the file directory, 
    #the averaging number in lat and lon for the "self" and "pairwise" subroutines, flag for sparse data cloud filtering
def cal_error_metric(dp, edges, start_scene, link, directory, N_pairwise, N_self):

    # make output matrix of zeros
    YY = zeros((edges + 1) * 2)
    if link.size != 0:

        # for each edge run cal_error_metric_pairwise and put the output into YY
        for i in range(edges):
            R_temp, RMSE_temp = emp.cal_error_metric_pairwise(int(link[i, 0]), int(link[i, 1]), dp[(2*link[i, 0])-2], dp[(2*link[i, 0])-1], dp[(2*link[i, 1])-2], dp[(2*link[i, 1])-1], directory, N_pairwise)
            YY[2 * i] = R_temp
            YY[(2 * i) + 1] = RMSE_temp
    
    # run cal_error_metric_self and put output into YY
    R_temp, RMSE_temp = ems.cal_error_metric_self(dp[(2 * start_scene) - 2], dp[(2 * start_scene) - 1], directory, N_self)
    YY[(2 * (edges + 1)) - 2] = R_temp
    YY[(2 * (edges + 1)) - 1] = RMSE_temp
    
    # return Y
    return YY
    
