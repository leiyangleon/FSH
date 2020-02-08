# extract_scatterplot_density.py
# Yang Lei, Microwave Remote Sensing Lab, University of Massachusetts
# November 3, 2015

# This script calculates the 2D histogram of the scatter plot between pairs of forest height, 
# and returns the forest height pairs with relatively large density. This script was incorporated
# to replace the previous remove_outlier.py for sparse lidar samples since through the use of this function, the current 
# version of code is capable of distinguishing forest disturbance and forest height estimation. 

#!/usr/bin/python



import numpy as np


def extract_scatterplot_density(x, y, bin_size=100, threshold=0.5):

	values, xedges, yedges = np.histogram2d(x, y, bin_size)
	xbin_center = xedges[0:-1] + (xedges[1]-xedges[0])/2
	ybin_center = yedges[0:-1] + (yedges[1]-yedges[0])/2
	max_den = np.max(values)
	threshold_den = max_den * threshold
	[BCX, BCY] = np.meshgrid(xbin_center, ybin_center)
	values = values.transpose()
	IND_den = (values >= threshold_den)
	Hm_den = BCX[IND_den]
	Pm_den = BCY[IND_den]
	return Hm_den, Pm_den
