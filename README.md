# Forest Stand Height (FSH) Python Scripts

Produced by the University of Massachusetts Microwave Remote Sensing Laboratory

113 Knowles Engineering Building, University of Massachusetts at Amherst, Amherst, MA, USA 01003


Scripts written Summer 2015 by Tracy Whelen, based on Matlab code written by Yang Lei. Then modified by Yang Lei in 2015 through 2017.
Some scripts contain code written by Diya Chowdhury, and Gerard Ruiz Carregal


Contact Information:
Python code -- Yang Lei (leiyangfrancis@gmail.com), Tracy Whelen (twhelen@engin.umass.edu) 
Forest Stand Height Model -- Yang Lei (leiyangfrancis@gmail.com), Paul Siqueira (siqueira@ecs.umass.edu)


Citation: 

https://github.com/leiyangleon/FSH/


References: 

1. Lei, Y. and Siqueira, P., 2014. Estimation of forest height using spaceborne repeat-pass L-Band InSAR correlation magnitude over the US State of Maine. Remote Sensing, 6(11), pp.10252-10285.
2. Lei, Y. and Siqueira, P., 2015. An automatic mosaicking algorithm for the generation of a large-scale forest height map using spaceborne repeat-pass InSAR correlation magnitude. Remote Sensing, 7(5), pp.5639-5659.
3. (**MOST RECENT**) Y. Lei, P. Siqueira, N. Torbick, M. Ducey, D. Chowdhury and W. Salas, "Generation of Large-Scale Moderate-Resolution Forest Height Mosaic With Spaceborne Repeat-Pass SAR Interferometry and Lidar," in IEEE Transactions on Geoscience and Remote Sensing, DOI: 10.1109/TGRS.2018.2860590
URL: http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8439086&isnumber=4358825


License:

Forest Stand Height (FSH) Python Scripts. This software performs the automated forest height inversion and mosaicking from spaceborne repeat-pass L-band HV-pol InSAR correlation magnitude data (e.g. JAXA’s ALOS-1/2, and the future NASA-ISRO’s NISAR) that have been pre-processed by JPL’s ROI_PAC and/or ISCE programs.

Copyright (C) 2017  Yang Lei, Paul Siqueira, Tracy Whelen.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. 

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. 

You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.

=====================================================================================

# Table of Contents:

## I. Needed software packages and installation

## II. Instructions and runtime estimates

## III. List of python files and corresponding descriptions
    
   ### a. List of files
    
   ### b. File Descriptions
	

====================================================================================

## I. Needed software packages and installation

To run these python scripts the following software packages are needed:

Python (This code was developed and tested using Version 2.7)
Additional Python packages: NumPy, SciPy, SimPy, json, pillow, OsGeo/GDAL, simplekml

Note: This software was originally developed and tested on a Windows machine. Python code should be runnable from a Linux operating system. However, it was indeed tested on Macintosh computers running various OS X (e.g. 10.9, 10.10, 10.11). If help with setting up on Linux is needed please contact the developers and it can be put on the list of future improvements.

- For Mac users: it is strongly recommended to use MacPorts (https://www.macports.org/) to install Python along with the above Python modules, since it is very easy (no more then 3 command lines for each module) and organized.

- For Windows users: it is recommend to use the Anaconda distribution of python, as it is designed for scientific computing, and comes with Numpy, SciPy, json, and pillow.

  The simplekml package can be found at www.simplekml.com (follow the download links to https://pypi.python.org/pypi/simplekml). Alternatively you can use pip install simplekml from the Anaconda command line.

  OsGeo/GDAL can be installed on Windows using the following steps
	
      1) Download and install Microsoft Visual C++ for the Windows version you have.
      2) Go to http://www.gisinternals.com/release.php and click on the link corresponding to your MSVC version and Windows 32/64 bit version
      3) From the link above Download and install the 'gdal-111-1400-core.msi' and 'GDAL-1.11.1.win32-py2.7.msi' (or whatever verion of python you have, eg py3.3)
      4) From the link above Download and extract the dir 'release-1600-gdal-1-11-1-mapserver-6-4-1'
      5) Once the dir is unzipped, copy all files in dir bin/gdal/python/* to C:\Users\keb\Anaconda\Lib\site-packages\ (or the site-packages directory of whatever python distribution you are using)
      6) Add 'Program Files/GDAL' to the system PATH variable (NOT the user PATH variable) in system settings (thru control panel > advanced settings)
      7) To test if everything is installed correctly:
        at the cmd prompt (cmd.exe) type 'gdalinfo -h' and you should get some options such as -stats etc 
        in python type 'from osgeo import gdal' and you shouldn't get an error.
		


=====================================================================================

## II. Instructions and runtime estimates:

The overall workflow for the forest stand height model is as follows:
1. Run ROI_PAC or ISCE (see parameter notes below)
2. Crop the ROI_PAC/ISCE output to eliminate the image margins (run standalone CROP_ROIPAC.py or CROP_ISCE.py)
3. Geocode the ROI_PAC/ISCE output
4. Run the Forest Stand Height python documents that are described in this document
5. Create the mosaic of the generated forest height maps for all of the scenes


---------------------------------------------------------------------------------------------------

In step 2, for ROI_PAC-processed results, run the following command line:

python directory_of_scripts/CROP_ROIPAC.py dirname date1 date2

	dirname	-	the directory where the ROI_PAC amp/cor files are located
	date1	-	date for 1st SAR acquisition
	date2	-	date for 2nd SAR acquisition

while for ISCE-processed results, run the following command within the execution of insarApp.py

python directory_of_scripts/CROP_ISCE.py

***Note: the amount of margin to be cropped are hardcoded based on the ALOS SAR image dimension, and needs to be adjusted for ALOS-2 and the future NISAR image.  ***

---------------------------------------------------------------------------------------------------

In step 5, run the following command to create the final mosaic map of FSH as a single GeoTiff file

python directory_of_scripts/create_mosaic.py directory mosaicfile listoffiles
	
	directory	-	the same root directory as forest_stand_height.py executes
	mosaicfile	-	file name of the final mosaic file
	listoffiles	-	paths to all the forest height maps that are to be combined, e.g. in the format of “file1 file2 file3 …”


---------------------------------------------------------------------------------------------------

The scripts used in Step 4 are organized so that they can be run at the command line by a single command, shown here:

python forest_stand_height.py scenes edges start_scene iterations link_file flag_file ref_file mask_file file_directory output_file_types [--Nd_pairwise] [--Nd_self] [--N_pairwise] [--N_self] [--bin_size] [--flag_sparse] [--flag_diff] [--flag_error] [—numLooks] [—noiselevel] [--flag_proc] [--flag_grad]

The parameters listed in brackets are optional. All other paramters require input.

Exact parameter definitions and full descriptions can be found in the File Description section below.

The input files that need to be in file_directory are:

  - flag_file - a text file that lists all the flags and corresponding full file names and associated file information (dates, scene location (frame#, orbit#), polarization), e.g. 
  
      001 890_120_20070727_HV_20070911_HV 070727 070911 890 120 HV
  
      002 890_119_20070710_HV_20071010_HV 070710 071010 890 119 HV
  
      003 890_118_20070708_HV_20070923_HV 070708 070923 890 118 HV
  
  - ref_file - reference tree height data (Lidar or field inventory) in raster format. Currently the code is set up to use a GeoTIFF file, but other reference data in raster format could potentially be used with some code adjustments. Margin/NoData values should be sent to NaN or some number less than zero. 	
	
  - mask_file - landcover mask that excludes all water areas and areas of human disturbance (urban, agriculture). Currently set up to be a GeoTIFF file. Other reference data in raster format could potentially be used with some code adjustments. File must be in degrees (i.e., EPSG 4326). This file is optional (although recommended to use). If unused input "-" in place of the file name for the command line arguments. Both the lidar data and the forest/non_forest mask are better to be resampled to the comparable (preferably the same) resolution as the InSAR image.
	
  - link_file - a text file that lists all the edge scene pairs. Each line consists of the two numbers that correspond to the flag numbers for those two scenes. (e.g. "2 1" would be the line for the edge of the above scenes 001 and 002). If using a single ALOS scene this file is unneeded, and input "-" instead of the file name for the command line arguments.	
	
  - file_directory - the root directory that consists of the individual scenes-directories. Each scene should have a directory named f#1_o#2 where #1 is the frame number and #2 is the orbit number (e.g. “f890_o120” for the above scene 001). This directory will both contain the input ROI_PAC/ISCE files, as well be the output location for all files that are associated with only that scene.

---------------------------------------------------------------------------------------------------


For each ROI_PAC-processed scene, the following files should be located in a directory with the format “f#1_o#2/int_date1_date2":
		
    date1_date2_baseline.rsc
		
    date1-date2.amp.rsc
		
    date1-date2_2rlks.amp.rsc
		
    date1-date2-sim_SIM_2rlks.int.rsc
		
    geo_date1-date2_2rlks.amp
		
    geo_date1-date2_2rlks.cor	
		
    geo_date1-date2_2rlks.cor.rsc
		
*** Note: ROI_PAC’s process_2pass.pl should be run with 2 range looks and 10 azimuth looks in both coherence estimation and multi-looking  (equivalent to a 30m-by-30m area for JAXA’s ALOS), with the following lines added to the process file:
		
    Rlooks_int = 2
		
    Rlooks_sim = 2
		
    Rlooks_sml = 2
		
    pixel_ratio = 5

A 5-point triangle window is hardcoded in ROI_PAC, which is equivalent to a 2-point rectangle window. For further details on running ROI_PAC see the ROI_PAC manual. ***


For each ISCE-processed scene, the following files should be located in a directory with the format “f#1_o#2/int_date1_date2":
		
    isce.log
		
    resampOnlyImage.amp.geo
		
    resampOnlyImage.amp.geo.xml
		
    topophase.cor.geo	
		
    topophase.cor.geo.xml
		
*** Note: ISCE’s insarApp.py should be run with 2 range looks and 10 azimuth looks in both coherence estimation and multi-looking (equivalent to a 30m-by-30m area for JAXA’s ALOS), with the following lines added to the process file:
		
    <property name="range looks">1</property>
		
    <property name="azimuth looks">5</property>

A 5-point triangle window is hardcoded in ISCE, which is equivalent to a 2-point rectangle window. The .amp/.cor images then need to be multilooked by a factor of two. For further details on running ISCE see the ISCE manual. ***


The location of the output files depends on whether they are related to the overall processing of the entire data set, or are directly associated with a single scene. Examples of each would be the SC iteration files as a general output, and a single forest stand height image as a scene-specific output. The general outputs will be stored in a directory named "output" located within the main file directory (file_directory). The scene specific outputs will be stored with the other scene data as described earlier.

---------------------------------------------------------------------------------------------------


Here is an an example run of the model using a three scene dataset (in the test example folders), consisting of a central scene with overlapping NASA’s LVIS LiDAR data and two adjacent scenes. All five possible final output data types are produced. Runtimes are based off of running the model on a Macintosh 64-bit machine with 16GB RAM, and an Intel Core i7 @ 2.8 GHz processor.
Note: Runtime does not increase linearly with each additional scene. Runtime for most of the steps are linear in the number of scenes, however, the core part of the inversion & mosaicking depends on the number of edges, which increases a bit faster as the number of scenes increases. 

A sample run is given below by referring to the directory containing all the python scripts:


- For ROI_PAC-processed files on a Windows machine:

python directory_of_scripts/forest_stand_height.py 3 2 2 5 “linkfile.txt” “flagfile.txt” “Howland_LVIS_NaN.tif” “Maine_NLCD2011_nonwildland.tif” “C:\\Users\\...directory_of_files...\\” “gif json kml mat tif” --flag_proc=0


- For ISCE-processed files on a Windows machine:

python directory_of_scripts/forest_stand_height.py 3 2 2 5 “linkfile.txt” “flagfile.txt” “Howland_LVIS_NaN.tif” “Maine_NLCD2011_nonwildland.tif” “C:\\Users\\...directory_of_files...\\” “gif json kml mat tif” --flag_proc=1


- For ROI_PAC-processed files on a Mac machine:

python directory_of_scripts/forest_stand_height.py 3 2 2 5 “linkfile.txt” “flagfile.txt” “Howland_LVIS_NaN.tif” “Maine_NLCD2011_nonwildland.tif” “/Users/...directory_of_files.../” “gif json kml mat tif” --flag_proc=0


- For ISCE-processed files on a Mac machine:

python directory_of_scripts/forest_stand_height.py 3 2 2 5 “linkfile.txt” “flagfile.txt” “Howland_LVIS_NaN.tif” “Maine_NLCD2011_nonwildland.tif” “/Users/...directory_of_files.../” “gif json kml mat tif” --flag_proc=1


The scripts are also able to be run with a single radar scene. To do this use “-“ instead of a link_file name, and in the input have 0 edges. 
	- Example: python forest_stand_height.py 1 0 1 5 - “flagfile.txt” “Howland_LVIS_NaN.tif” “Maine_NLCD2011_nonwildland.tif” “/Users/...directory_of_files.../” “gif json kml mat tif” --flag_proc=1

*** make sure you use '\\' or '/' instead of '\' for directory name ***

---------------------------------------------------------------------------------------------------


This main script in turn calls seven other scripts with the total runtime around 23 minutes 22 secs for the test example of mosaicking three ALOS InSAR scenes:

- auto_tree_height_many() - extracts data from ROI_PAC/ISCE output files and formats them for use in the rest of the scripts (15 secs)

- intermediate() - calculates the overlap between each pair of images (12 mins 17 secs)

- auto_mosaicking_new() - runs iterations of mosaicking (~34 secs per iteration, or 2 mins 49 secs total)

- write_deltaSC() - calculates the temporal change parameters based on the final iteration (less than a second)

- write_mapfile_new() - calculates and writes the tree height map to a file (7 mins 55 secs)

- Use of --flag_diff calls write_diff_height_map() to produce the forest differential height map between the radar and overlapping lidar images (1 sec).

- Use of --flag_error calls cal_error_metric() to produce the error metric file that can be used for plotting figures (5 secs).

Detailed information on each of the substeps can be found in the file descriptions below.




=====================================================================================


## III. List of python files and corresponding descriptions


### IIIa. List of Files:


arc_sinc.py

auto_mosaicking_new.py

auto_tree_height_many.py

auto_tree_height_single_ROIPAC.py

auto_tree_height_single_ISCE.py

cal_error_metric.py

cal_error_metric_pairwise.py

cal_error_metric_self.py

cal_KB.py

cal_KB_pairwise_new.py

cal_KB_self_new.py

extract_scatterplot_density.py

flag_scene_file.py

forest_stand_height.py

intermediate.py

intermediate_pairwise.py

intermediate_self.py

ls_deltaSC.py

mean_wo_nan.py

read_geo_data.py

read_linkfile.py

read_rsc_data.py

remove_corr_bias.py

remove_nonforest.py

remove_outlier.py

write_deltaSC.py

write_diff_height_map.py

write_file_type.py

write_mapfile_new.py


---------------------------------------------------------------------------------------------------

### IIIb. File Descriptions:

arc_sinc.py - Calculates the inverse sinc function

Input: 

	x (numpy array) - x values for inverse sinc function
  
	c_param (float) - C parameter from the Forest Stand Height model
  
Output:
	
  y (numpy array) - y values of inverse sinc function satisfying x=sinc(y/C)


-------------------------------------------------------------

auto_mosaicking_new.py - calculates the S and C parameters automatically through iterations for all the scenes in preparation for forest height estimation

Input:

	scenes (int) - number of scenes in the data set
  
	edges (int) - number of edges (aka scene-scene borders)
  
	start_scene (int) - flag value of the central scene that overlaps the ground truth data
  
	N (int) - number of iterations to run the nonlinear least squares part of the model
  
	linkarray (numpy array) - array of the scene pairs that correspond to each edge in the format array([[scene1, scene2], [scene1, scene3], etc])
  
	directory (string) - directory path of where the input and output files are located
  
	[--Nd_pairwise] (int) - pixel-averaging number for image fitting between two overlapped radar scenes (default=20)
  
	[--Nd_self] (int) - pixel-averaging number for image fitting between single radar scene and the overlapped ground truth data (default=10)
  
	[--bin_size] (int) - bin size for density calculation in scatter plot fitting when ground truth data are sparse (default=100)
  
	[--flag_sparse] (int) - flag for sparse data cloud fitting (input 0 or 1, default=0)
  
Output: Script produces iteration files (.json format; e.g. “SC_#_iter.json” for “#”th iteration) that store the increment steps of S and C parameters and the residual; no values are returned by the function

To run alone at the command line type: 

python directory_of_scripts/auto_mosaicking_new.py scenes edges start_scene N linkfile directory

In this case linkfile is the file name of the file that lists all the edge scene pairs, and all other parameters are as described above.

-------------------------------------------------------------

auto_tree_height_many.py - For each scene runs auto_tree_height_single, and then saves the output correlation magnitudes, kz, and coordinates in a .mat file, and geo data (lines, samples, corner latitude and longitude, and latitude and longitude step size) in a text file

Input:

	scenes (int) - number of scenes in the data set
  
	flagfile (string) - file name of the file that lists all the scene flags and corresponding full file names and associated file date (dates, scene location (frame#,orbit#), polarization)
  
	directory (string) - directory path of where the input and output files are located
  
	[--numLooks] (int) - number of looks in the correlation estimation (default=20)
  
	[--flag_proc] (int) - flag for InSAR processor selection (input 0 for ROI_PAC or 1 for ISCE, default=0)
  
	[--flag_grad] (int) - flag for correction of large-scale temporal change gradient (input 0 or 1, default=0)
  
Output:

	scenename_orig.mat - .mat file that stores correlation map, kz value, and corner coordinates
  
	scenename_geo.txt - text file that stores the geodata (width, lines, corner lat and lon, and lat and lon step values)
  
	
To run alone at the command line type: 

python directory_of_scripts/auto_tree_height_many.py scenes flagfile directory

All three parameters are as described above.

-------------------------------------------------------------

auto_tree_height_single_ROIPAC.py - Extracts the correlation magnitude, kz parameter, corner coordinates, and geo location data from the ROI_PAC output files

Input:

	directory (string) - directory path of where the input and output files are located
  
	date1 (string) - date of the first image of the interferogram (format however they are listed in the scene data text file, such as 070911 for September 11, 2007)
  
	date2 (string) - date of the second image of the interferogram (same format as date1)
  
	numLooks (int) - number of looks in the correlation estimation
  
	noiselevel (float) - sensor thermal noise level (ALOS’s value hardcoded as default)
  
	flag_grad (int) - flag for correction of large-scale temporal change gradient (input 0 or 1)
  
Output:

	corr_vs (numpy array) - aray of the correlation magnitudes
  
	kz (float) - kz parameter
  
	coords (numpy array) - array of max lat and lon values in the format [north, south, west, east]
  
	geo_width (int) - number of columns of image data
  
	geo_nlines (int) - number of rows of image data
  
	corner_lat (float) - max latitude value (north)
  
	corner_lon (float) - min latitude value (west)
  
	step_lat (float) - latitude pixel size in decimal degrees
  
	step_lon (float) - longitude pixel size in decimal degrees
  

-------------------------------------------------------------
auto_tree_height_single_ISCE.py - Extracts the correlation magnitude, kz parameter, corner coordinates, and geo location data from the ISCE output files

Input:

	directory (string) - directory path of where the input and output files are located
  
	date1 (string) - date of the first image of the interferogram (format however they are listed in the scene data text file, such as 070911 for September 11, 2007)
	
	date2 (string) - date of the second image of the interferogram (same format as date1)
	
	numLooks (int) - number of looks in the correlation estimation
	
	noiselevel (float) - sensor thermal noise level (ALOS’s value hardcoded as default if no value provided)
	
	flag_grad (int) - flag for correction of large-scale temporal change gradient (input 0 or 1)

Output:
	
  	corr_vs (numpy array) - aray of the correlation magnitudes
	
  	kz (float) - kz parameter
	
  	coords (numpy array) - array of max lat and lon values in the format [north, south, west, east]
	
  	geo_width (int) - number of columns of image data
	
  	geo_nlines (int) - number of rows of image data
	
  	corner_lat (float) - max latitude value (north)
	
  	corner_lon (float) - min latitude value (west)
	
  	step_lat (float) - latitude pixel size in decimal degrees
	
  	step_lon (float) - longitude pixel size in decimal degrees


-------------------------------------------------------------


cal_error_metric.py - Calculates the R and RMSE error metrics for the model

Input:
	
  	dp (numpy array) - array of increment steps of S and C parameter values
	
  	edges (int) - number of edges (aka scene-scene borders)
	
  	start_scene (int) - flag value of the central scene that overlaps the ground truth data
	
  	link (numpy array) - array of the scene pairs that correspond to each edge in the format array([[scene1, scene2], [scene1, scene3], etc])
	
  	directory (string) - directory path of where the input and output files are located
	
  	N_pairwise (int) - pixel-averaging number for scatter plot
	
  	N_self (int) - pixel-averaging number for scatter plot

Output:
	
  	YY (numpy array) - array of R and RMSE values


-------------------------------------------------------------


cal_error_metric_pairwise_new.py - Calculates the R and RMSE error metrics for a pair of overlapping images

Input:
	
  	scene1 (int) - flag value of one scene in the pair
	
  	scene2 (int) - flag value of the other scene in the pair
	
  	deltaS1 (float) - change in S value for one scene in the pair
	
  	deltaC1 (float) - change in C value for one scene in the pair
	
  	deltaS2 (float) - change in S value for the other scene in the pair
	
  	deltaC2 (float) - change in C value for the other scene in the pair
	
  	directory (string) - directory path of where the input and output files are located
	
  	N_pairwise (int) - pixel-averaging number for scatter plot
	
  	link files: one for each overlapping edge region, with the filename format scene1_scene2.mat (generated in previous steps)

Output:
	
  	R (float) - R parameter for this edge
	
  	RSME (float) - RSME parameter for this edge
	
  	R_RSME_files: one for each edge with the filename format scene1_scene2_I1andI2.json


-------------------------------------------------------------


cal_error_metric_self_new.py - Calculates the R and RMSE error metrics for the central scene and overlapping ground truth data

Input:
	
  	deltaS2 (float) - change in S value for the central scene
	
  	deltaC2 (float) - change in C value for the central scene
	
  	directory (string) - directory path of where the input and output files are located
	
  	N_self (int) - pixel-averaging number for scatter plot
	
  	self.mat: link file for the central scene-ground truth overlap region (generated in previous steps)

Output:
	
  	R (float) - R parameter for this edge
	
  	RSME (float) - RSME parameter for this edge
	
  	R_RSME_file: self_I1andI2.json


-------------------------------------------------------------


cal_KB.py - Calculates the k and b values for the Forest Stand Height model

Input:
	
  	dp (numpy array) - array of increment steps of S and C parameter values
	
  	edges (int) - number of edges (aka scene-scene borders)
	
  	start_scene (int) - flag value of the central scene that overlaps the ground truth data
	
  	link (numpy array) - array of the scene pairs that correspond to each edge in the format array([[scene1, scene2], [scene1, scene3], etc])
	
  	directory (string) - directory path of where the input and output files are located
	
  	Nd_pairwise (int) - pixel-averaging number for image fitting between two overlapped radar scenes
	
  	Nd_self (int) - pixel-averaging number for image fitting between single radar scene and the overlapped ground truth data
	
  	bin_size (int) - bin size for density calculation in scatter plot fitting
	
  	flag_sparse (int) - flag for sparse data cloud filtering (input 0 or 1)

Output:
	
  	YY (numpy array) - array of k and b values


-------------------------------------------------------------


cal_KB_pairwise_new.py - Calculates the k and b values for a pair of overlapping images

Input:
	
  	scene1 (int) - flag value of one scene in the pair
	
  	scene2 (int) - flag value of the other scene in the pair
	
  	deltaS1 (float) - change in S value for one scene in the pair
	
  	deltaC1 (float) - change in C value for one scene in the pair
	
  	deltaS2 (float) - change in S value for the other scene in the pair
	
  	deltaC2 (float) - change in C value for the other scene in the pair
	
  	directory (string) - directory path of where the input and output files are located
	
  	Nd_pairwise (int) - pixel-averaging number for image fitting between two overlapped radar scenes
	
  	bin_size (int) - bin size for density calculation in scatter plot fitting
	
  	link files: one for each overlapping edge region, with the filename format scene1_scene2.mat (generated in previous steps)

Output:
	
  	k (float) - k parameter for this edge
	
  	b (float) - b parameter for this edge


-------------------------------------------------------------


cal_KB_self_new.py - Calculates the k and b values for the central scene and overlapping LiDAR

Input:
	
  	deltaS2 (float) - change in S value for the central scene
	
  	deltaC2 (float) - change in C value for the central scene
	
  	directory (string) - directory path of where the input and output files are located
	
  	Nd_self (int) - pixel-averaging number for image fitting between single radar scene and the overlapped ground truth data
	
  	bin_size (int) - bin size for density calculation in scatter plot fitting
	
  	flag_sparse (int) - flag for sparse data cloud filtering (input 0 or 1)
	
  	self.mat: link file for the central scene-ground truth overlap region (generated in previous steps)

Output:
	
  	k (float) - k parameter for this edge
	
  	b (float) - b parameter for this edge


-------------------------------------------------------------

extract_scatterplot_density.py - calculates the 2D histogram of the scatter plot between pairs of forest height, and returns the forest height pairs with relatively large density

Input:
	
  	x (numpy array) - array of x values of points
	
  	y (numpy array) - array of y values of points
	
  	bin_size (int) - bin size for density calculation in scatter plot fitting (default = 100)
	
  	threshold (float) - density threshold (default = 0.5)

Output:
	
  	Hm_den (numpy array) - array of x values of the points with densities above the inputted threshold
	
  	Pm_den (numpy array) - array of y values of the points with densities above the inputted threshold


-------------------------------------------------------------


flag_scene_file.py - reads and extracts data from the file that associates flag numbers with other interferogram file data. Each line in the input textfile should be formatted as 'flag flagfilename date1 date2 frame orbit polarization'.

Input:
	
  	flagfilename (string) - file name of the file that lists all the flags and corresponding full file names and associated file date (dates, scene location (frame#,orbit#), polarization)
	
  	flag (int) - flag of the desired scene
	
  	directory (string) - directory path of where the input and output files are located

Output:
	
  	data_array (list) - list of the data associated with the given flag number


-------------------------------------------------------------


forest_stand_height.py - Main program, runs the processing steps between ROI_PAC/ISCE output and Forest Stand Height (FSH) map after inversion and mosaicking

Input:
	
  	All input is given as a command line argument in the following order:
	
  	scenes (int) - number of scenes in the data set
	
  	edges (int) - number of edges (aka scene-scene borders)
	
  	start_scene (int) - flag value of the central scene that overlaps the ground truth (e.g. LiDAR, field) data
	
  	iterations (int) - number of iterations to run the nonlinear least squares part of the model
	
  	linkfilename (string) - file name of the file that lists all the edge scene pairs or '-' if processing a single scene
	
  	flagfile (string) - file name of the file that lists all the scene flags and corresponding full file names and associated file date (dates, scene location (frame#,orbit#), polarization)
	
  	ref_file (string) - filename of reference data raster file (ground truth data, e.g. LiDAR, field)
	
  	maskfile (string) - filename of the mask file that excludes all non-forest areas (mask excluding water and human disturbed areas such as urban and agriculture is also acceptable; if no mask is a available input '-' as the filename)
	
  	file_directory (string) - directory path of where the input and output files are located
	
  	filetypes (string) - list of the desired output file types formatted as a single string (e.g. "kml json tif")
	
  	[--Nd_pairwise] (int) - optional pixel-averaging parameter for edge fitting (default=20)
	
  	[--Nd_self] (int) - optional pixel-averaging parameter for central scene fitting (default=10)
	
  	[--N_pairwise] (int) - optional pixel-averaging parameter for edge error metrics (default=20)
	
  	[--N_self] (int) - optional pixel-averaging parameter for central scene error metrics (default=10)
	
  	[—-bin_size] (int) - optional bin size for density calculation in sparse data cloud fitting (default=100)
	
  	[--flag_sparse] (int) - optional flag for sparse data cloud filtering (choose 0 or 1, default=0)
	
  	[--flag_diff] (int) - optional flag for exporting differential height maps (choose 0 or 1, default=0)
	
  	[--flag_error] (int) - optional flag for exporting .json error metric files (choose 0 or 1, default=0)
	
  	[--numLooks] (int) - number of looks in the correlation estimation (default=20)
	
  	[--noiselevel] (float) - sensor thermal noise level (ALOS’s value hardcoded as default if no value provided)
	
  	[--flag_proc] (int) - flag for InSAR processor selection (choose 0 for ROI_PAC or 1 for ISCE, default=0)
	
  	[--flag_grad] (int) - flag for correction of large-scale temporal change gradient (choose 0 or 1, default=0)

Output: no direct output (all file output created in subprocesses)


-------------------------------------------------------------


intermediate.py - Creates the overlap areas between scenes

Input:
	
  	edges (int) - number of edges (aka scene-scene borders)
	
  	start_scene (int) - flag value of the central scene that overlaps the ground truth data
	
  	linkarray (numpy array) - array of the scene pairs that correspond to each edge in the format array([[scene1, scene2], [scene1, scene3], etc])
	
  	maskfile (string) - filename of the mask file that excludes all non-forest areas (mask excluding water and human disturbed areas such as urban and agriculture is also acceptable)
	
  	flagfile (string) - file name of the file that lists all the scene flags and corresponding full file names and associated file date (dates, scene location (frame#,orbit#), polarization)
	
  	ref_file (string) - filename of the reference data raster file
	
  	directory (string) - directory path of where the input and output files are located

Output: no direct output (all file output created in subprocesses)

To run alone at the command line type: 

python directory_of_scripts/intermediate.py edges start_scene linkfile maskfile flagfile ref_file directory

In this case linkfile is the file name of the file that lists all the edge scene pairs, and all other parameters are as described above.


-------------------------------------------------------------


intermediate_pairwise.py - Calculates the overlap between a pair of scenes

Input:
	
  	flag1 (int) - flag value of one scene in the pair
	
  	flag2 (int) - flag value of the other scene in the pair
	
  	flagfile (string) - file name of the file that lists all the scene flags and corresponding full file names and associated file date (dates, scene location (frame#,orbit#), polarization)
	
	  maskfile (string) - filename of the mask file that excludes all non-forest areas (mask excluding water and human disturbed areas such as urban and agriculture is also acceptable)

	  directory (string) - directory path of where the input and output files are located

	  filename1_orig.mat: correlation map and associated parameters for the first scene (generated in previous steps)

	  filename2_orig.mat: correlation map and associated parameters for the second scene (generated in previous steps)

Output:
	
  	link files: one for each overlapping edge region, with the filename format flag1_flag2.mat


-------------------------------------------------------------


intermediate_self.py - Calculates the overlap between the central scene and the ground truth data

Input:
	
	  start_scene (int) - flag value of the central scene that overlaps the ground truth data

	  flagfile (string) - file name of the file that lists all the scene flags and corresponding full file names and associated file date (dates, scene location (frame#,orbit#), polarization)

	  directory (string) - directory path of where the input and output files are located

	  filename_orig.mat: correlation map and associated parameters for the central scene (generated in previous steps)

	  reference data raster file (already exists; main input)

Output:
	
  	self.mat: link file for the central scene-ground truth overlap region


-------------------------------------------------------------


ls_deltaSC.py - Obtains the current S and C parameters by running nonlinear least squares on the previous iteration

Input:
	
	  dp (numpy array) - array of increment steps of S and C parameter values

	  edges (int) - number of edges (aka scene-scene borders)

	  scenes (int) - number of scenes in the data set

	  start_scene (int) - flag value of the central scene that overlaps the ground truth data

	  linkarray (numpy array) - array of the scene pairs that correspond to each edge in the format array([[scene1, scene2], [scene1, scene3], etc])

	  directory (string) - directory path of where the input and output files are located

	  Nd_pairwise (int) - pixel-averaging number for image fitting between two overlapped radar scenes 

	  Nd_self (int) - pixel-averaging number for image fitting between single radar scene and the overlapped ground truth data 

	  bin_size (int) - bin size for density calculation in scatter plot fitting

	  flag_sparse (int) - flag for sparse data cloud filtering (input 0 or 1)

Output:
	
	  changeSC (numpy array) - updated S and C parameters as referenced to the average S (=0.6) and C (=13)

	  res (float) - residual k and b error compared to k = 1 and b = 0


-------------------------------------------------------------


mean_wo_nan.py - Calculates the mean of the values in an array excluding NaN values

Input:
	
  	A (numpy array) - input array of values

Output:
	
  	mean of B (A excluding NaN values) (float)


-------------------------------------------------------------


read_geo_data.py - Reads the lat/long, step size, and the image width and lines from either a geotiff or a text file based on ROI_PAC output

Input:
	
	  coord_file (string) - file name of the input data file with the location information (lat/long, step size, image size)

	  directory (string) - directory path of where the input and output files are located

Output:
	
	  width (int) - width/number of columns of the image

	  nlines (int) - lines/number of rows of the image

	  corner_lat (float) - latitude of the upper left corner

	  corner_long (float) - longitude of the upper left corner

	  post_lat (float) - latitude step size

	  post_long (float) - longitude step size


-------------------------------------------------------------


read_linkfile.py - Reads the edge scene pairs from a text file and into a numpy array

Input:
	
	  edges (int) - number of edges (aka scene-scene borders)

	  filename (string) - file name of the file that lists all the edge scene pairs

	  directory (string) - directory path of where the input and output files are located

Output:
	
  	linkarray (numpy array) - array of the scene pairs that correspond to each edge in the format array([[scene1, scene2], [scene1, scene3], etc])

To run alone at the command line type: 

python directory_of_scripts/read_linkfile.py edges filename directory

All three parameters are as described above.


-------------------------------------------------------------


read_rsc_data.py - reads a parameter from the inputted ROI_PAC .rsc text output file

Input:
	
	  filename (string) - file name of the ROI_PAC text output file containing the desired parameter (may include subdirectories containing the ROI_PAC output files - everything lower than the main file directory)

	  directory (string) - directory path of where the input and output files are located

	  param (string) - name of the desired parameter

Output:
	
  	result (float) - paramter value


-------------------------------------------------------------


remove_corr_bias.py - Remove the ROI_PAC/ISCE associated correlation bias

Input:
	
	  C (numpy array) - correlation magnitude array

	  numLooks (int) - number of looks in the correlation estimation

Output:
	
  	YC (numpy array) - correlation magnitude array (with bias removed)


-------------------------------------------------------------


remove_nonforest.py - Mask out non-forest portions of the scenes

Input:
	
	  I (numpy array) - the image data

	  func_coords (numpy array) - array of corner coordinates

	  maskfile (string) - filename of the mask file that excludes all non-forest areas (mask excluding water and human disturbed areas such as urban and agriculture is also acceptable)

	  directory (string) - directory path of where the input and output files are located

Output:
	
  	O (numpy array) - image without the non-forest sections


-------------------------------------------------------------


remove_outlier.py - Remove values that have too few neighbors within a certain radius

Input:
	
	  x (numpy array) - array of x values of points

	  y (numpy array) - array of y values of points

	  win_size (float) - window size to search for neighboring points (defaults to 0.5)

	  threshold (int) - number of neighboring points needed within the window to not count as an outlier (defaults to 5)

Output:
	
	  XX (numpy array) - array of x values of the points excluding those counted as outliers

	  YY (numpy array) - array of y values of the points excluding those counted as outliers


-------------------------------------------------------------


write_deltaSC.py - Calculates and writes the relative S and C values (as referenced to the average values: S=0.6, C=13) based on the final iteration output

Input:
	
	  scenes (int) - number of scenes in the data set

	  N (int) - number of iterations to run the nonlinear least squares part of the model

	  flagfile (string) - file name of the file that lists all the scene flags and corresponding full file names and associated file date (dates, scene location (frame#,orbit#), polarization)

	  directory (string) - directory path of where the input and output files are located

	  SC_#_iter.json: final iteration file (generated in previous steps)

Output:
	
  	one file per scene that contains delta S and C; file name format is "scenename_tempD.json"
	
To run alone at the command line type: 

python directory_of_scripts/write_deltaSC.py scenes N flagfile directory

All four parameters are as described above.


-------------------------------------------------------------


write_diff_height_map.py - Makes the differential height map (value is ground truth - InSAR height) and writes it to a file
	
	  start_scene (int) - flag value of the central scene that overlaps the ground truth data

	  reffile (string) - reference filename containing ground truth data

	  flagfile (string) - file name of the file that lists all the scene flags and corresponding full file names and associated file date (dates, scene location (frame#,orbit#), polarization)

	  maskfile (string) - filename of the mask file that excludes all non-forest areas (mask excluding water and human disturbed areas such as urban and agriculture is also acceptable) (optional - if no mask available use '-' as an input to forest_stand_height.py)

	  directory (string) - directory path of where the input and output files are located

	  output_files (string) - list of the desired output file types formatted as a single string (e.g. "kml json tif")

Output: no direct output (all file output created in write_file_type.py)


-------------------------------------------------------------


write_file_type.py - Writes the input array (the tree height map or the differential height map) to one of five file types based on the input parameters

Input:
	
	  data (numpy array) - array to be written to the file

	  outtype (string) - string to signify which input (tree height “stand_height” or differential height “diff_height”) is being output

	  filename (string) - scene file name

	  directory (string) - directory path of where the input and output files are located

	  filetype (string) - file extension for the desired output file type (.gif, .json, .kml, .mat, and .tif accepted -> input without the "." (e.g. "kml" instead of ".kml")
	  
	  coords (numpy array) - array of max lat and lon values in the format [north, south, west, east]
	
	  reffile (string) - reference filename containing ground truth data (optional - only needed for differential height map)

Output:
	
  	output files(s) of the array image saved in the file type specified in the input


-------------------------------------------------------------


write_mapfile_new.py - Makes the tree height map and writes it to an file

Input:
	
	  scenes (int) - number of scenes in the data set

	  flagfile (string) - file name of the file that lists all the scene flags and corresponding full file names and associated file date (dates, scene location (frame#,orbit#), polarization)

	  maskfile (string) - filename of the mask file that excludes all non-forest areas (mask excluding water and human disturbed areas such as urban and agriculture is also acceptable) (optional - if no mask available use '-' as an input to forest_stand_height.py)

	  directory (string) - directory path of where the input and output files are located

	  output_files (string) - list of the desired output file types formatted as a single string (e.g. "kml json tif")

	  scenename_orig.mat: correlation map and associated parameters for the central scene (generated in previous steps)

	  scenename_tempD.json: delta S and C files produced (generated in previous steps)

Output: no direct output (all file output created in write_file_type.py)

