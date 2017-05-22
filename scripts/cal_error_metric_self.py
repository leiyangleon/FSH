# cal_error_metric_self.py
# Yang Lei, Microwave Remote Sensing Lab, University of Massachusetts
# Tracy Whelen, Microwave Remote Sensing Lab, University of Massachusetts
# December 8, 2015

# This calculates R measure and RMSE between the central image and LiDAR strip.

#!/usr/bin/python
from numpy import * 
import math as mt   
import json
import arc_sinc as arc
import mean_wo_nan as mwn
import remove_outlier as rout
import pdb
import scipy.io as sio

# Define cal_error_metric_self function
# input parameters are the change in s and c, the file directory, the averaging number in lat and lon, flag for sparse data cloud filtering
def cal_error_metric_self(deltaS2, deltaC2, directory, N_self):
    
    # Load and read data from .json file
    # Image data is stored as a list and must be turned back into an array
    # Samples and lines are calculated from the shape of the images
#    selffile = open(directory + "output/" + "self.json")
#    selffile_data = json.load(selffile)
#    selffile.close()
#    image1 = array(selffile_data[0])
#    image2 = array(selffile_data[1])
#    lines = int(image1.shape[0])
#    samples = int(image1.shape[1])

    # Load and read data from .mat file
    # Samples and lines are calculated from the shape of the images
    selffile_data = sio.loadmat(directory + "output/" + "self.mat")
    image1 = selffile_data['I1']
    image2 = selffile_data['I2']
    lines = int(image1.shape[0])
    samples = int(image1.shape[1])

    # Set the S and C parameters to the average S and C plus the delta values
    S_param2 = 0.65 + deltaS2
    C_param2 = 13 + deltaC2

    # Create gamma and run arc_since for image2   
    gamma2 = image2.copy()
    gamma2 = gamma2 / S_param2
    image2 = arc.arc_sinc(gamma2, C_param2)
    image2[isnan(gamma2)] = nan

    # Partition image into subsections for noise suppression (multi-step process)
    # Create M and N which are the number of subsections in each direction
    # NX and NY are the subsection dimensions
    NX = N_self
    NY = N_self
    M = fix(lines / NY)
    N = fix(samples / NX)

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
#    IND2 = logical_not(IND2);
#    I1m_trunc = I1m_trunc[IND2, ...]
#    I2m_trunc = I2m_trunc[IND2, ...]

    
    # Call remove_outlier on these cells unless when there are only a few of lidar samples that are sparsely distributed
##    if sparse_lidar_flag != 1:
##        I1m_trunc, I2m_trunc = rout.remove_outlier(I1m_trunc, I2m_trunc, 0.5, 2)
    
    R = corrcoef(I1m_trunc,I2m_trunc)
    R = R[0,1]
    RMSE = sqrt(sum((I1m_trunc-I2m_trunc)**2)/I1m_trunc.size)
    
    #Export the pair of heights for future scatter plot
    filename = "self_I1andI2.json"
    R_RSME_file = open(directory + "output/" + filename, 'w')
    json.dump([I1m_trunc.tolist(), I2m_trunc.tolist()], R_RSME_file)
    R_RSME_file.close()
    
    
    return R, RMSE
