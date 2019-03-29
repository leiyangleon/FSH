# intermediate_pairwise.py
# Tracy Whelen, Microwave Remote Sensing Lab, University of Massachusetts
# December 8, 2015
# Yang Lei, Jet Propulsion Labortary, California Institute of Technology
# May 18, 2017




# This script is the python version of intermediate_pairwise.m, which calculates the overlap
# between each pair of scenes. The python verion reads the data directly from auto_tree_height_single, 
# rather than from an intermediary file.

#!/usr/bin/python

from numpy import *
import scipy.io as sio
import json
from scipy.interpolate import griddata
import flag_scene_file as fsf
import remove_nonforest as rnf

# Define intermediate_pairwise function
# Input parameters are the flags for each image for that edge, scene data file, non-forest maskfile, and the file directory
def intermediate_pairwise(flag1, flag2, flagfile, maskfile, directory):

    # Get flag-scene file data
    scene1_data = fsf.flag_scene_file(flagfile, flag1, directory)
    scene2_data = fsf.flag_scene_file(flagfile, flag2, directory)

    # Set file names based on flags
    filename1 = scene1_data[1]
    filename2 = scene2_data[1]
    
    # Set the image folder names
    image1_folder = "f" + scene1_data[4] + "_o" + scene1_data[5] + "/"
    image2_folder = "f" + scene2_data[4] + "_o" + scene2_data[5] + "/"

#    # Read in .mat/Gamma version of input data
#    # Load first image file and associated parameters
#    # kz must be extracted from the array
#    file1 = sio.loadmat(directory + filename1 + '.mat')
#    corr1 = file1['corr_vs']
#    kz1 = file1['kz'][0][0]
#    coords1 = file1['coords'][0]
#    
#    # Load second image file and associated parameters
#    # kz must be extracted from the array
#    file2 = sio.loadmat(directory + filename2 + '.mat')
#    corr2 = file2['corr_vs']
#    kz2 = file2['kz'][0][0]
#    coords2 = file2['coords'][0]

    # Load first image file and associated parameters
    
##    file1 = open(directory + image1_folder + filename1 + "_orig.json")
##    file1_data = json.load(file1)
##    file1.close()

    file1 = sio.loadmat(directory + image1_folder + filename1 + "_orig.mat")
    corr1 = file1['corr_vs']
    kz1 = file1['kz'][0][0]
    coords1 = file1['coords'][0]

    # Load second image file and associated parameters
    
##    file2 = open(directory + image2_folder + filename2 + "_orig.json")
##    file2_data = json.load(file2)
##    file2.close()

    file2 = sio.loadmat(directory + image2_folder + filename2 + "_orig.mat")
    corr2 = file2['corr_vs']
    kz2 = file2['kz'][0][0]
    coords2 = file2['coords'][0]
    
##    # Set parameter values based on file1_data
##    corr1 = array(file1_data[0])
##    kz1 = float(file1_data[1])
##    coords1 = array(file1_data[2])
## 
##    # Set parameter values based on file2_data   
##    corr2 = array(file2_data[0])
##    kz2 = float(file2_data[1])
##    coords2 = array(file2_data[2])
    
    # Set D constant --- D = 1 arc second
    D = 2.7777778 * (10**-4)

    # Remove non-forest from both images
    if maskfile != '-':
        corr1 = rnf.remove_nonforest(corr1, coords1, maskfile, directory)
        corr2 = rnf.remove_nonforest(corr2, coords2, maskfile, directory)
    
    # Set the image boundaries
    north1 = coords1[0]
    south1 = coords1[1]
    west1 = coords1[2]
    east1 = coords1[3]
    north2 = coords2[0]
    south2 = coords2[1]
    west2 = coords2[2]
    east2 = coords2[3]

    # Determine boundaries of the overlap area
    overlap_north = min(north1, north2)
    overlap_south = max(south1, south2)
    overlap_east = min(east1, east2)
    overlap_west = max(west1, west2)

    # Calculate overlap boundaries in coordinates of each image (ex image1[1000-1200] vs image2[0-200])
    xw1 = int(round(((overlap_west - west1) / D) + 1))
    xe1 = int(round(((overlap_east - west1) / D) + 1))
    xn1 = int(round((-(overlap_north - north1) / D) + 1))
    xs1 = int(round((-(overlap_south - north1) / D) + 1))
    xw2 = int(round(((overlap_west - west2) / D) + 1))
    xe2 = int(round(((overlap_east - west2) / D) + 1))
    xn2 = int(round((-(overlap_north - north2) / D) + 1))
    xs2 = int(round((-(overlap_south - north2) / D) + 1))

    # Set overlap sections from each image
    I1 = corr1[xw1-1:xe1][:, xn1-1:xs1]
    I2 = corr2[xw2-1:xe2][:, xn2-1:xs2]
    
    # Set average S and C parameters based on the average S and C (0<s<1, 0<c<20 so s=0.65 and c=13)
    S_param1 = 0.65
    C_param1 = 13
    S_param2 = 0.65
    C_param2 = 13

    # Create grid for image1
    [Dy1, Dx1] = I1.shape
    x1 = linspace(0, 1, Dx1)
    y1 = linspace(0, 1, Dy1)
    [X1, Y1] = meshgrid(x1, y1)
    
    # Create grid for image2
    [Dy2, Dx2] = I2.shape    
    x2 = linspace(0, 1, Dx2)
    y2 = linspace(0, 1, Dy2)
    [X2, Y2] = meshgrid(x2, y2)

    # Set NaN values to -100 to avoid interpolation errors
    I1[isnan(I1)] = -100
    I2[isnan(I2)] = -100
    
    # Co-register the two images
    I2 = griddata((X2.flatten(), Y2.flatten()), I2.flatten(), (X1, Y1), method='nearest')

    # Reset NaN values
    IND1 = (I1 == -100)
    IND2 = (I2 == -100)
    IND = logical_or(IND1, IND2)
    I1[IND] = NaN
    I2[IND] = NaN
    
    # Save link file using JSON
    # linkfilename = "%s_%s.json" % (int(flag1), int(flag2))
    # linkfile = open(directory + "output/" + linkfilename, 'w')
    # json.dump([I1.tolist(), I2.tolist(), S_param1, C_param1, S_param2, C_param2], linkfile)
    # linkfile.close()
    
    # Save link file using MAT
    linkfilename = "%s_%s.mat" % (int(flag1), int(flag2))
    linkfile = directory + "output/" + linkfilename
    sio.savemat(linkfile,{'I1':I1,'I2':I2})
    
        
        
