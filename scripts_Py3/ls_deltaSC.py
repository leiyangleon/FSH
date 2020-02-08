# ls_deltaSC.py
# Tracy Whelen, Microwave Remote Sensing Lab, University of Massachusetts
# Yang Lei, Microwave Remote Sensing Lab, University of Massachusetts
# November 16, 2015

# This is the python version of ls_deltaSC.m, which runs least squares on the change in S and C parameters

#!/usr/bin/python
from numpy import *
import cal_KB as cKB
import pdb
import scipy.io as sio


# define ls_deltaSC function
# input paramters are the dp matrix, number of edges, number of scenes, start_scene, an array of the edge scene pairs, the file directory, 
    # averaging numbers in lat/lon for "self" and "pairwise" fitting (Nd_pairwise, Nd_self), bin_size for density calculation in scatter plot fitting, 
    # flag for sparse data cloud filtering
def ls_deltaSC(dp, edges, scenes, start_scene, linkarray, directory, Nd_pairwise, Nd_self, bin_size, flag_sparse):

    # run cal_KB
    y = cKB.cal_KB(dp, edges, start_scene, linkarray, directory, Nd_pairwise, Nd_self, bin_size, flag_sparse)

    # Create a blank array for the Jacobi matrix
    jacobi = zeros(4 * scenes * (edges + 1)) #(2 * (edges + 1)) * (2 * scenes)
    jacobi = reshape(jacobi, (2 * (edges + 1), scenes * 2))
    


    # Fill in the Jacobi matrix
    for i in range(scenes):
        # fill K section
        temp = dp.copy()
        temp[2 * i] = temp[2 * i] + 0.1 # i and i+1 instead of i-1 and i due to index 0 vs 1
        temp = cKB.cal_KB(temp, edges, start_scene, linkarray, directory, Nd_pairwise, Nd_self, bin_size, flag_sparse)
        jacobi[:, 2 * i] = reshape(((temp - y) / 0.1), (2 * (edges + 1), )) # reshape temp-y part to 1D (a) instead of 2D (ax1)


        # fill B section       
        temp = dp.copy()
        temp[(2 * i) + 1] = temp[(2 * i) + 1] + 1
        temp = cKB.cal_KB(temp, edges, start_scene, linkarray, directory, Nd_pairwise, Nd_self, bin_size, flag_sparse)
        jacobi[:, (2 * i) + 1] = reshape(((temp - y) / 1), (2 * (edges + 1), ))
    
    # Create matrix of target K and B values (K = 1, B = 0 in order K-B-K-B-K-B...)
    target = zeros((edges + 1) * 2)
    target[::2] = 1
    
##    print "pre-inversion !!!"

    # Calculate the change in S and C 
    changeSC = dot(dot(linalg.inv(dot(jacobi.conj().transpose(), jacobi)), jacobi.conj().transpose()), (target - y))

#    pdb.set_trace()
##    print "post-inversion !!!"

##    pdb.set_trace()
##    print changeSC
##    sio.savemat('/Users/yanglei/Desktop/JACOBI.mat',{'jacobi':jacobi})
    
    changeSC = changeSC + dp
    YY = cKB.cal_KB(changeSC, edges, start_scene, linkarray, directory, Nd_pairwise, Nd_self, bin_size, flag_sparse)
    res = sum((YY - target)**2)

    # return changeSC and res
    return changeSC, res
