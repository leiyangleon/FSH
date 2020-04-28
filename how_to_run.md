
## Notes:

***1. Preprocessing scripts (in the folder "ISCE_processing_scripts") have been added for using ISCE's insarApp (ISCE v2.0, v2.1 and v2.2) and stripmapApp (ISCE v2.2, v2.3) with only 1 command line for actual data processing after appropriate setup. Test examples of using insarApp and stripmapApp are provided as well. All the [historial ISCE versions](https://winsar.unavco.org/software/isce) and the [current ISCE version](https://github.com/isce-framework/isce2) can be used to process ALOS-1 and ALOS-2 stripmap InSAR data.***

***2. The Python 3 scripts are ready to use. Please use the folder "scripts_Py3" instead of the one using Python 2 ("scripts"). This Python 3 version of the scripts can be run the same as the Python 2 version (replacing "python" in all the following commands with "python3"), or can run in Google Colaboratory (with unix operating system) using [Exercise_1_FSH on the SERVIR Global GitHub](https://github.com/SERVIR/ForestStandHeight).***

***3. Only 2 command lines are involved to automatically perform the forest height inversion and mosaicking task (1 command for FSH inversion and 1 for FSH mosaicking).***

***4. In a future release of the software, backscatter-inverted mosaic map will also be incorporated to this InSAR coherence-based mosaic map to generate a final mosaic of FSH (see the [citation](https://ieeexplore.ieee.org/document/8439086)).***
  
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

Python (This code was developed and tested using Version 2.7 and has been updated to Version 3.6+)

Additional Python packages: NumPy, SciPy, SimPy, json, pillow, OsGeo/GDAL, simplekml, mpmath

***Note: This software was originally developed and tested on a Windows machine. Python code was tested on Macintosh computers running various OS X (e.g. 10.9-10.14) as well as Linux operating system.***

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

In step 1, users may find online support and guidance running ROI_PAC (the command "process_2pass.pl"). Since it only supports ALOS-1 data and has been deprecated, we do not cover the details for running it. Instead, we provide the details along with the scripts for running ISCE, with the precursor being ROI_PAC. ISCE supports JAXA's ALOS-1 and ALOS-2 data and also NASA's future NISAR mission. ISCE's application "insarApp.py" is valid for ISCE v2.0, v2.1 and v2.2, while deprecated for v2.3. "insarApp.py" uses the amplitude cross-correlation (ampcor) to coregister the two radar images. In contrast, starting from v2.2, ISCE started to replace the role of "insarApp.py" with "stripmapApp.py", which uses the radar observing geometry along with dense ampcor + rubbersheeting (to apply the ampcor-determined offsets) for image coregistration. As each method has its own merit, and so far neither is absolutely better than the other, we include both options and leave the quality assessment to the users. Since ISCE v2.2 is the only version of ISCE that supports both "insarApp.py" and "stripmapApp.py", we tested the following scripts with this version only. However, the scripts are meant to work with all versions of ISCE v2+.

All the ISCE preprocessing scripts can be found under the folder "ISCE_processing_scripts/".

Below are the preparation for using the ISCE applications "insarApp" and "stripmapApp" to process radar data for FSH.

	0) Copy the 7 scripts (CROP_ISCE_insarApp.py, CROP_ISCE_stripmapApp.py, format_insarApp_xml.py, format_stripmapApp_xml.py, MULTILOOK_FILTER_ISCE.py, single_scene_insarApp.py, single_scene_stripmapApp.py) under "ISCE_processing_scripts" to any local folder that is on the environmental variables PATH and PYTHONPATH

For using ISCE's insarApp, 

	1) Replace ISCE/isce/components/isceobj/InsarProc/runCoherence.py with ISCE_processing_scripts/insarApp_substitute/runCoherence.py
	
For using ISCE's stripmapApp,

	2) Replace ISCE/isce/components/isceobj/StripmapProc/runCoherence.py with ISCE_processing_scripts/stripmapApp_substitute/runCoherence.py

	3) Replace ISCE/isce/components/isceobj/StripmapProc/runGeocode.py with ISCE_processing_scripts/stripmapApp_substitute/runGeocode.py

	4) Replace ISCE/isce/components/isceobj/StripmapProc/runPreprocessor.py with ISCE_processing_scripts/stripmapApp_substitute/runPreprocessor.py

	5) Replace ISCE/isce/applications/stripmapApp.py with ISCE_processing_scripts/stripmapApp_substitute/stripmapApp.py

To run the scripts for actual processing (with ALOS-1 data as an example), we need to put two unzipped ALOS-1 data folders (with the folder name formatted as "ALPSRP*-L1.0") in the same directory, e.g. test_data. For running insarApp, one only needs to type the following command line:
	
	single_scene_insarApp.py -f test_data

and for running stripmapApp, one can type:

	single_scene_stripmapApp.py -f test_data

***Note: in this tutorial, there is only 1 command line involved for the actual processing using ISCE's insarApp or stripmapApp after the above 0-5) preparation, which is done once and for all.*** 

***Note: some of the parameters in the 7 scripts of 0) are hardcoded for the ALOS data as an example of using the scripts, and needs to be adjusted for ALOS-2 and the future NISAR data.***

***Note: for better use of updated functions and also to be compatible with future ISCE releases, it is thus recommended not to simply replace those ISCE original files in 1-5) but to directly add the newly added lines into the ISCE original files. Those newly added lines start and end with the pattern shown below:***
	
    # NEW COMMANDS added by YL --start
    	...
    # NEW COMMANDS added by YL --end


---------------------------------------------------------------------------------------------------

In step 2 and step 3, for ROI_PAC-processed results, run the following command line:

	python directory_of_scripts/CROP_ROIPAC.py dirname date1 date2

	dirname	-	the directory where the ROI_PAC amp/cor files are located
	date1	-	date for 1st SAR acquisition
	date2	-	date for 2nd SAR acquisition

for cropping the image margin and refer to online ROI_PAC guidance for the geocoding command "geocode.pl" (not included here). 

For ISCE-processed results, the cropping and geocoding have been included in the above ISCE processing (Step 1), i.e. 1) for insarApp and 2) for stripmapApp in Step 1. 

***Note: the amount of margin to be cropped are hardcoded based on the ALOS SAR image dimension, and needs to be adjusted for ALOS-2 and the future NISAR image.***

---------------------------------------------------------------------------------------------------

In step 5, run the following command to create the final mosaic map of FSH as a single GeoTiff file

	python directory_of_scripts/create_mosaic.py directory mosaicfile listoffiles
	
	directory	-	the same root directory as forest_stand_height.py executes
	mosaicfile	-	file name of the final mosaic file
	listoffiles	-	paths to all the forest height maps that are to be combined, e.g. in the format of “file1 file2 file3 …”


---------------------------------------------------------------------------------------------------

The scripts used in Step 4 are organized so that they can be run at the command line by a single command, shown here:

	python forest_stand_height.py scenes edges start_scene iterations link_file flag_file ref_file mask_file file_directory output_file_types [--Nd_pairwise] [--Nd_self] [--N_pairwise] [--N_self] [--bin_size] [--flag_sparse] [--flag_diff] [--flag_error] [—numLooks] [—noiselevel] [--flag_proc] [--flag_grad]

The parameters listed in square brackets are optional. All other paramters require input.

Exact parameter definitions and full descriptions can be found in the File Description section below.

The input files that need to be in file_directory are:

  - flag_file - a text file that lists all the flags and corresponding full file names and associated file information (dates, scene location (frame#, orbit#), polarization), e.g. 
  
      001 890_120_20070727_HV_20070911_HV 070727 070911 890 120 HV
  
      002 890_119_20070710_HV_20071010_HV 070710 071010 890 119 HV
  
      003 890_118_20070708_HV_20070923_HV 070708 070923 890 118 HV
  
  - ref_file - reference tree height data (Lidar or field inventory) in raster format. Currently the code is set up to use a GeoTIFF file, but other reference data in raster format could potentially be used with some code adjustments. Margin/NoData values should be sent to NaN or some number less than zero. 	
	
  - mask_file - landcover mask that excludes all water areas and areas of human disturbance (urban, agriculture). Currently set up to be a GeoTIFF file. Other reference data in raster format could potentially be used with some code adjustments. File must be in degrees (i.e., EPSG 4326). This file is optional (although recommended to use). If unused input "-" in place of the file name for the command line arguments. Both the lidar data and the forest/non_forest mask are better to be resampled to the comparable (preferably the same) resolution as the InSAR image.
	
  - link_file - a text file that lists all the edge scene pairs. Each line consists of the two numbers that correspond to the flag numbers for those two scenes. (e.g. "2 1" would be the line for the edge of the above scenes 001 and 002). If using a single ALOS scene this file is unneeded, and input "-" instead of the file name for the command line arguments.	
	
  - file_directory - the root directory that consists of the individual scenes-directories. Each scene should have a directory named "f$frame_o$orbit" (e.g. “f890_o120” for the above scene 001). This directory will both contain the input ROI_PAC/ISCE files, as well be the output location for all files that are associated with only that scene.

---------------------------------------------------------------------------------------------------


For each ROI_PAC-processed scene, the following files should be located in a directory with the format “f$frame_o$orbit/int_$date1_$date2":
		
    $date1_$date2_baseline.rsc
		
    $date1-$date2.amp.rsc
		
    $date1-$date2_2rlks.amp.rsc
		
    $date1-$date2-sim_SIM_2rlks.int.rsc
		
    geo_$date1-$date2_2rlks.amp
		
    geo_$date1-$date2_2rlks.cor	
		
    geo_$date1-$date2_2rlks.cor.rsc
		
***Note: ROI_PAC’s process_2pass.pl should be run with 2 range looks and 10 azimuth looks in both coherence estimation and multi-looking  (equivalent to a 30m-by-30m area for JAXA’s ALOS), with the following lines added to the process file:***
		
    Rlooks_int = 2
		
    Rlooks_sim = 2
		
    Rlooks_sml = 2
		
    pixel_ratio = 5

***A 5-point triangle window is hardcoded in ROI_PAC, which is equivalent to a 2-point rectangle window. For further details on running ROI_PAC see the ROI_PAC manual.***


For each ISCE-processed scene, the following files should be located in a directory with the format “f$frame_o$orbit/int_$date1_$date2":
		
    *Proc.xml (insarProc.xml for insarApp and stripmapProc.xml for stripmapApp)
		
    resampOnlyImage.amp.geo
		
    resampOnlyImage.amp.geo.xml
		
    topophase.cor.geo	
		
    topophase.cor.geo.xml
		
***Note: ISCE’s insarApp.py or stripmapApp.py should be run with 2 range looks and 10 azimuth looks in both coherence estimation and multi-looking (equivalent to a 30m-by-30m area for JAXA’s ALOS), with the following lines added to the process file:***
		
    <property name="range looks">1</property>
		
    <property name="azimuth looks">5</property>

***A 5-point triangle window is hardcoded in ISCE, which is equivalent to a 2-point rectangle window. The .amp/.cor images then need to be multilooked by a factor of two. All of the above parameter setup along with margin cropping, multilooking and geocoding have already been included in the folder ISCE_processing_scripts (Step 1). For further details on running ISCE see the [ISCE manual](https://github.com/isce-framework/isce2).***


The location of the output files depends on whether they are related to the overall processing of the entire data set, or are directly associated with a single scene. Examples of each would be the SC iteration files as a general output, and a single forest stand height image as a scene-specific output. The general outputs will be stored in a directory named "output" located within the main file directory (file_directory). The scene specific outputs will be stored with the other scene data as described earlier.

---------------------------------------------------------------------------------------------------


Here is an an example run of the model using a three scene dataset (in the test example folders), consisting of a central scene with overlapping NASA’s LVIS LiDAR data and two adjacent scenes. All five possible final output data types are produced. Runtimes are based off of running the model on a Macintosh 64-bit machine with 16GB RAM, and an Intel Core i7 @ 2.8 GHz processor.

***Note: Runtime does not increase linearly with each additional scene. Runtime for most of the steps are linear in the number of scenes, however, the core part of the inversion & mosaicking depends on the number of edges, which increases a bit faster as the number of scenes increases.***

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

- Example: 

		python forest_stand_height.py 1 0 1 5 - “flagfile.txt” “Howland_LVIS_NaN.tif” “Maine_NLCD2011_nonwildland.tif” “/Users/...directory_of_files.../” “gif json kml mat tif” --flag_proc=1

***Note: make sure you use '\\\\' or '/' instead of '\\' for directory path***

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
