# cal_KB_pairwise_new.py
# Tracy Whelen, Microwave Remote Sensing Lab, University of Massachusetts
# Yang Lei, Microwave Remote Sensing Lab, University of Massachusetts
# November 16, 2015

# This is the python version of cal_KB_pairwise_new.m, which calculates k and b between image pairs.

#!/usr/bin/python
from numpy import *
import scipy.io as sio
import math as mt 
import json
import arc_sinc as arc
import mean_wo_nan as mwn
import extract_scatterplot_density as espd
import remove_outlier as rout




# Define cal_KB_pairwise_new function
# input parameters are the scene number, change in s and c for each of the two scenes in the pair, the file directory, 
    # averaging number in lat/lon for fitting (Nd_pairwise), bin_size for density calculation in scatter plot fitting
def cal_KB_pairwise_new(scene1, scene2, deltaS1, deltaC1, deltaS2, deltaC2, directory, Nd_pairwise, bin_size):

    # Set main file name string as scene1_scene2
    file_str = str(scene1) + '_' + str(scene2)
   
    
    
    # selffile = open(directory + "output/" + file_str + ".json")
    # selffile_data = json.load(selffile)
    # selffile.close()
    # image1 = array(selffile_data[0])
    # image2 = array(selffile_data[1])
    # lines = int(image1.shape[0])
    # samples = int(image1.shape[1])
    
    # Load and read data from .mat file
    # Samples and lines are calculated from the shape of the images
    selffile_data = sio.loadmat(directory + "output/" + file_str + ".mat")
    image1 = selffile_data['I1']
    image2 = selffile_data['I2']
    lines = int(image1.shape[0])
    samples = int(image1.shape[1])
    
    # S and C parameters are the average S and C plus the delta value
    S_param1 = 0.65 + deltaS1
    S_param2 = 0.65 + deltaS2
    C_param1 = 13 + deltaC1
    C_param2 = 13 + deltaC2
    
    # Create gamma and run arc_since for image1
    gamma1 = image1.copy()
    gamma1 = gamma1 / S_param1
    image1 = arc.arc_sinc(gamma1, C_param1)
    image1[isnan(gamma1)] = nan

    # Create gamma and run arc_since for image2     
    gamma2 = image2.copy()
    gamma2 = gamma2 / S_param2
    image2 = arc.arc_sinc(gamma2, C_param2)
    image2[isnan(gamma2)] = nan
    
    
    # Partition image into subsections for noise suppression (multi-step process)
    # Create M and N which are the number of subsections in each direction; fix() rounds towards zero
    # NX and NY are the subsection dimensions
    NX = Nd_pairwise
    NY = Nd_pairwise
    M = int(fix(lines / NY))
    N = int(fix(samples / NX))

    # Create JM and JN, which is the remainder after dividing into subsections
    JM = lines % NY
    JN = samples % NX

    # Select the portions of images that are within the subsections
    image1 = image1[0:lines - JM][:, 0:samples - JN]
    image2 = image2[0:lines - JM][:, 0:samples - JN]

    # Split each image into subsections and run mean_wo_nan on each subsection
    
    # Declare new arrays to hold the subsection averages
    image1_means = zeros((M, N))
    image2_means = zeros((M, N))
    
    # Processing image1
    # Split image into sections with NY number of rows in each
    image1_rows = split(image1, M, 0)
    for i in range(M):
        # split each section into subsections with NX number of columns in each
        row_array = split(image1_rows[i], N, 1)
        # for each subsection shape take the mean without NaN and save the value in another array
        for j in range(N):
            image1_means[i, j] = mwn.mean_wo_nan(row_array[j]) 

    # Processing image2
    # Split image into sections with NY number of rows in each
    image2_rows = split(image2, M, 0)
    for i in range(M):
        # split each section into subsections with NX number of columns in each
        row_array = split(image2_rows[i], N, 1)
         # for each subsection shape take the mean without NaN and save the value in another array
        for j in range(N):
            image2_means[i, j] = mwn.mean_wo_nan(row_array[j])           

    
    # Make an array for each image of where mean > 0 for both images
    IND1 = logical_and((image1_means > 0), (image2_means > 0))
    I1m_trunc = image1_means[IND1, ...]
    I2m_trunc = image2_means[IND1, ...]
    
    # Remove the overestimation at low height end (usually subjet to imperfection of the mask 
    # over water bodies, farmlands and human activities) and the saturation points over the forested areas due to logging
#    IND2 = logical_or((I1m_trunc < 5), (I2m_trunc > (mt.pi * C_param2 - 1)))
#    IND3 = logical_or((I2m_trunc < 5), (I1m_trunc > (mt.pi * C_param1 - 1)))
#    IND4 = logical_or(IND2, IND3)
#    IND4 = logical_not(IND4);
#    I1m_trunc = I1m_trunc[IND4, ...]
#    I2m_trunc = I2m_trunc[IND4, ...]

    I1m_trunc, I2m_trunc = rout.remove_outlier(I1m_trunc, I2m_trunc, 0.5, 2)
    
    # Extract density values from the 2D scatter plot
##    I1m_den, I2m_den = espd.extract_scatterplot_density(I1m_trunc, I2m_trunc, bin_size)

    I1m_den = I1m_trunc   
    I2m_den = I2m_trunc

    # Calculate the covariance matrix of the data with outliers removed
    cov_matrix = cov(I1m_den, I2m_den)
     
    
    # Calculate the eigenvalues
    dA, vA = linalg.eig(cov_matrix)
    
    
#    # print the elliptical ratio (from 0 to 1; the lower value, the better elliptical shape -> the more robust estimation)
#    elliptical_ratio = dA.min() / dA.max()
#    print "Elliptical ratio (i.e. b/a of the ellipse): %f" % elliptical_ratio
#    if elliptical_ratio > 0.5:
#        print "Warning: Relatively bad elliptical shape!"

    # Calculate K and B
    # K is based on whichever value in dA is the largest
    if (dA[0] > dA[1]): # dA[0] is largest
        K = vA[1, 0] / vA[0, 0]
    else: # dA[1] is largest
        K = vA[1, 1] / vA[0, 1]
    B = 2 * mean(I1m_den - I2m_den) / mean(I1m_den + I2m_den)
    
    return K, B
     
