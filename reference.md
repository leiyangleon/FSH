# III. List of python files and corresponding descriptions


## IIIa. List of Files:


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

## IIIb. File Descriptions:

### arc_sinc.py - Calculates the inverse sinc function

Input: 

	x (numpy array) - x values for inverse sinc function
  
	c_param (float) - C parameter from the Forest Stand Height model
  
Output:
	
  y (numpy array) - y values of inverse sinc function satisfying x=sinc(y/C)


-------------------------------------------------------------

### auto_mosaicking_new.py - calculates the S and C parameters automatically through iterations for all the scenes in preparation for forest height estimation

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

### auto_tree_height_many.py - For each scene runs auto_tree_height_single, and then saves the output correlation magnitudes, kz, and coordinates in a .mat file, and geo data (lines, samples, corner latitude and longitude, and latitude and longitude step size) in a text file

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

### auto_tree_height_single_ROIPAC.py - Extracts the correlation magnitude, kz parameter, corner coordinates, and geo location data from the ROI_PAC output files

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
### auto_tree_height_single_ISCE.py - Extracts the correlation magnitude, kz parameter, corner coordinates, and geo location data from the ISCE output files

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


### cal_error_metric_pairwise.py - Calculates the R and RMSE error metrics for a pair of overlapping images

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


### cal_error_metric_self.py - Calculates the R and RMSE error metrics for the central scene and overlapping ground truth data

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


### cal_KB.py - Calculates the k and b values for the Forest Stand Height model

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


### cal_KB_pairwise_new.py - Calculates the k and b values for a pair of overlapping images

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


### cal_KB_self_new.py - Calculates the k and b values for the central scene and overlapping LiDAR

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

### extract_scatterplot_density.py - calculates the 2D histogram of the scatter plot between pairs of forest height, and returns the forest height pairs with relatively large density

Input:
	
  	x (numpy array) - array of x values of points
	
  	y (numpy array) - array of y values of points
	
  	bin_size (int) - bin size for density calculation in scatter plot fitting (default = 100)
	
  	threshold (float) - density threshold (default = 0.5)

Output:
	
  	Hm_den (numpy array) - array of x values of the points with densities above the inputted threshold
	
  	Pm_den (numpy array) - array of y values of the points with densities above the inputted threshold


-------------------------------------------------------------


### flag_scene_file.py - reads and extracts data from the file that associates flag numbers with other interferogram file data. Each line in the input textfile should be formatted as 'flag flagfilename date1 date2 frame orbit polarization'.

Input:
	
  	flagfilename (string) - file name of the file that lists all the flags and corresponding full file names and associated file date (dates, scene location (frame#,orbit#), polarization)
	
  	flag (int) - flag of the desired scene
	
  	directory (string) - directory path of where the input and output files are located

Output:
	
  	data_array (list) - list of the data associated with the given flag number


-------------------------------------------------------------


### forest_stand_height.py - Main program, runs the processing steps between ROI_PAC/ISCE output and Forest Stand Height (FSH) map after inversion and mosaicking

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


### intermediate.py - Creates the overlap areas between scenes

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


### intermediate_pairwise.py - Calculates the overlap between a pair of scenes

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


### intermediate_self.py - Calculates the overlap between the central scene and the ground truth data

Input:
	
	  start_scene (int) - flag value of the central scene that overlaps the ground truth data

	  flagfile (string) - file name of the file that lists all the scene flags and corresponding full file names and associated file date (dates, scene location (frame#,orbit#), polarization)

	  directory (string) - directory path of where the input and output files are located

	  filename_orig.mat: correlation map and associated parameters for the central scene (generated in previous steps)

	  reference data raster file (already exists; main input)

Output:
	
  	self.mat: link file for the central scene-ground truth overlap region


-------------------------------------------------------------


### ls_deltaSC.py - Obtains the current S and C parameters by running nonlinear least squares on the previous iteration

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


### mean_wo_nan.py - Calculates the mean of the values in an array excluding NaN values

Input:
	
  	A (numpy array) - input array of values

Output:
	
  	mean of B (A excluding NaN values) (float)


-------------------------------------------------------------


### read_geo_data.py - Reads the lat/long, step size, and the image width and lines from either a geotiff or a text file based on ROI_PAC output

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


### read_linkfile.py - Reads the edge scene pairs from a text file and into a numpy array

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


### read_rsc_data.py - reads a parameter from the inputted ROI_PAC .rsc text output file

Input:
	
	  filename (string) - file name of the ROI_PAC text output file containing the desired parameter (may include subdirectories containing the ROI_PAC output files - everything lower than the main file directory)

	  directory (string) - directory path of where the input and output files are located

	  param (string) - name of the desired parameter

Output:
	
  	result (float) - paramter value


-------------------------------------------------------------


### remove_corr_bias.py - Remove the ROI_PAC/ISCE associated correlation bias

Input:
	
	  C (numpy array) - correlation magnitude array

	  numLooks (int) - number of looks in the correlation estimation

Output:
	
  	YC (numpy array) - correlation magnitude array (with bias removed)


-------------------------------------------------------------


### remove_nonforest.py - Mask out non-forest portions of the scenes

Input:
	
	  I (numpy array) - the image data

	  func_coords (numpy array) - array of corner coordinates

	  maskfile (string) - filename of the mask file that excludes all non-forest areas (mask excluding water and human disturbed areas such as urban and agriculture is also acceptable)

	  directory (string) - directory path of where the input and output files are located

Output:
	
  	O (numpy array) - image without the non-forest sections


-------------------------------------------------------------


### remove_outlier.py - Remove values that have too few neighbors within a certain radius

Input:
	
	  x (numpy array) - array of x values of points

	  y (numpy array) - array of y values of points

	  win_size (float) - window size to search for neighboring points (defaults to 0.5)

	  threshold (int) - number of neighboring points needed within the window to not count as an outlier (defaults to 5)

Output:
	
	  XX (numpy array) - array of x values of the points excluding those counted as outliers

	  YY (numpy array) - array of y values of the points excluding those counted as outliers


-------------------------------------------------------------


### write_deltaSC.py - Calculates and writes the relative S and C values (as referenced to the average values: S=0.6, C=13) based on the final iteration output

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


### write_diff_height_map.py - Makes the differential height map (value is ground truth - InSAR height) and writes it to a file
	
	  start_scene (int) - flag value of the central scene that overlaps the ground truth data

	  reffile (string) - reference filename containing ground truth data

	  flagfile (string) - file name of the file that lists all the scene flags and corresponding full file names and associated file date (dates, scene location (frame#,orbit#), polarization)

	  maskfile (string) - filename of the mask file that excludes all non-forest areas (mask excluding water and human disturbed areas such as urban and agriculture is also acceptable) (optional - if no mask available use '-' as an input to forest_stand_height.py)

	  directory (string) - directory path of where the input and output files are located

	  output_files (string) - list of the desired output file types formatted as a single string (e.g. "kml json tif")

Output: no direct output (all file output created in write_file_type.py)


-------------------------------------------------------------


### write_file_type.py - Writes the input array (the tree height map or the differential height map) to one of five file types based on the input parameters

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


### write_mapfile_new.py - Makes the tree height map and writes it to an file

Input:
	
	  scenes (int) - number of scenes in the data set

	  flagfile (string) - file name of the file that lists all the scene flags and corresponding full file names and associated file date (dates, scene location (frame#,orbit#), polarization)

	  maskfile (string) - filename of the mask file that excludes all non-forest areas (mask excluding water and human disturbed areas such as urban and agriculture is also acceptable) (optional - if no mask available use '-' as an input to forest_stand_height.py)

	  directory (string) - directory path of where the input and output files are located

	  output_files (string) - list of the desired output file types formatted as a single string (e.g. "kml json tif")

	  scenename_orig.mat: correlation map and associated parameters for the central scene (generated in previous steps)

	  scenename_tempD.json: delta S and C files produced (generated in previous steps)

Output: no direct output (all file output created in write_file_type.py)
