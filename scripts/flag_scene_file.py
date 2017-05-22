# flag_scene_file.py
# Tracy Whelen, Microwave Remote Sensing Lab, University of Massachusetts
# December 8, 2015

# This script associates flag numbers with the name, dates, ALOS location (frame and orbit), and polarization of each scene
# Each line in the input textfile should be formatted as 'flag filename date1 date2 frame orbit polarization'

#!/usr/bin/python

# Define flag_scene_file function
# Input parameters are the textfile of all flag-file pairs and the flag associated with the desired image file
def flag_scene_file(flagfilename, flag, directory):
    
    # Open the file
    flagfile = open(directory + flagfilename)
    
    # Set default value for scene_file
    data_array = ["", "", "", "", "", ""]
    
    # For each line in the file compare the line flag with the input flag
    for line in flagfile:
        
        # Set the line values
        line = line.strip().split()
        lineflag = line[0]    
        
        # Compare line and input flags
        if int(lineflag) == flag:
            data_array = list(line)
            
    # Close file
    flagfile.close()
    
    # Print error message is input flag not found
    if(data_array[0] == ""):
        print ("ERROR: Invalid flag number for the given text file")
        
    # Return scene_file
    return data_array