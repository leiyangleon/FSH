# Yang Lei, Jet Propulsion Laboratory
# September, 2016

# This script crops the ISCE output files in radar coordinates by eliminating the erroneous edge effects.

#!/usr/bin/python
import numpy as np
import read_rsc_data as rrd
import sys
import pdb
import xml.etree.ElementTree as ET


# Extract ISCE parameters
xmlfile = "resampOnlyImage.amp.xml"
tree = ET.parse(xmlfile)
root = tree.getroot()
size_array = np.array([])
for size in root.iter('property'):
    if size.items()[0][1] == 'size':
        size_array = np.append(size_array, int(size.find('value').text))
width = size_array[0]
length = size_array[1]


nanval = 0


# Read amp files in radar coordinates
amp_file = np.fromfile("resampOnlyImage.amp", dtype='complex64')
inty = amp_file.reshape((length,width))

# Creating empty array for cropped square list
##inty[:88,:] = nanval
##inty[2744:,:] = nanval
##inty[:,:64] = nanval
##inty[:,2344:] = nanval

##inty[:799,:] = nanval
##inty[27120:,:] = nanval
##inty[:,:163] = nanval
##inty[:,4846:] = nanval

inty[:176,:] = nanval
inty[5488:,:] = nanval
inty[:,:163] = nanval
inty[:,4846:] = nanval


# Write output files
inty.tofile("resampOnlyImage.amp")
