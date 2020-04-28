# II. How to run FSH:

## Step 1: Generate the interferograms, see https://github.com/sgk0/FSH/edit/master/isce_preprocessing.md for help. 
### - If wanting to test the software on the example interferograms we provide (https://github.com/sgk0/FSH/blob/master/test_example_ISCE_stripmapApp/NOTES_ISCE_stripmapApp.txt), please skip ahead to Step 2a.

## Step 2a: Run the Forest Stand Height model.

### For the examples, we provide an exact command is provided in the text file ("NOTES_") placed in the respective example folder (i.e. "test_example_ISCE_stripmapApp")

The scripts are organized so that they can be run at the command line by a single command, shown here:

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

## Step 2b: Generate the mosaicked forest height maps as described in this document.

### For the examples, we provide an exact command is provided in the text file ("NOTES_") placed in the respective example folder (i.e. "test_example_ISCE_stripmapApp")

Run the following command to create the final mosaic map of FSH as a single GeoTiff file

	python directory_of_scripts/create_mosaic.py directory mosaicfile listoffiles
	
	directory	-	the same root directory as forest_stand_height.py executes
	mosaicfile	-	file name of the final mosaic file
	listoffiles	-	paths to all the forest height maps that are to be combined, e.g. in the format of “file1 file2 file3 …”
