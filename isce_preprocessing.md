# 2.1 Generate interferograms

The preprocessing [scripts](./ISCE_processing_scripts) first need to be set up properly, which is done once and for all. After setting up these scripts, there are three steps for the preprocessing. 

## 2.1.1 Preparation
## 2.1.2 Run ROI_PAC/ISCE (Step 1)
## 2.1.3 Crop the ROI_PAC/ISCE output to eliminate the image margins (Step 2)
## 2.1.4 Geocode the ROI_PAC/ISCE output (Step 3)

=====================================================================================


## 2.1.1 Preparation

In step 1, users may find online support and guidance running ROI_PAC (the command "process_2pass.pl"). Since it only supports ALOS-1 data and has been deprecated, we do not cover the details for running it. Instead, we provide the details along with the scripts for running ISCE, with the precursor being ROI_PAC. ISCE supports JAXA's ALOS-1 and ALOS-2 data and also NASA's future NISAR mission. ISCE's application "insarApp.py" is valid for ISCE v2.0, v2.1 and v2.2, while deprecated for v2.3. "insarApp.py" uses the amplitude cross-correlation (ampcor) to coregister the two radar images. In contrast, starting from v2.2, ISCE started to replace the role of "insarApp.py" with "stripmapApp.py", which uses the radar observing geometry along with dense ampcor + rubbersheeting (to apply the ampcor-determined offsets) for image coregistration. As each method has its own merit, and so far neither is absolutely better than the other, we include both options and leave the quality assessment to the users. Since ISCE v2.2 is the only version of ISCE that supports both "insarApp.py" and "stripmapApp.py", we tested the following scripts with this version only. However, the scripts are meant to work with all versions of ISCE v2+.

All the ISCE preprocessing scripts can be found under the [folder](./ISCE_processing_scripts).
Below are the steps we set up the updated ISCE applications (that requires replacing existing ISCE scripts) "insarApp" and "stripmapApp" to process radar (e.g. ALOS PALSAR in the test examples) data for FSH.


- Copy updated applications scripts,

      0) Copy the 7 scripts (CROP_ISCE_insarApp.py, CROP_ISCE_stripmapApp.py, format_insarApp_xml.py, \
      format_stripmapApp_xml.py, MULTILOOK_FILTER_ISCE.py, single_scene_insarApp.py, single_scene_stripmapApp.py) \
      under "ISCE_processing_scripts" to any local folder that is on the environmental variables PATH and PYTHONPATH

- For using ISCE's insarApp, 

      1) Replace ISCE/isce/components/isceobj/InsarProc/runCoherence.py with \
      ISCE_processing_scripts/insarApp_substitute/runCoherence.py
	
- For using ISCE's stripmapApp,

      2) Replace ISCE/isce/components/isceobj/StripmapProc/runCoherence.py with \
      ISCE_processing_scripts/stripmapApp_substitute/runCoherence.py

      3) Replace ISCE/isce/components/isceobj/StripmapProc/runGeocode.py with \
      ISCE_processing_scripts/stripmapApp_substitute/runGeocode.py

      4) Replace ISCE/isce/components/isceobj/StripmapProc/runPreprocessor.py with \
      ISCE_processing_scripts/stripmapApp_substitute/runPreprocessor.py

      5) Replace ISCE/isce/applications/stripmapApp.py with \
      ISCE_processing_scripts/stripmapApp_substitute/stripmapApp.py



## Step 1: Run ROI_PAC or ISCE

To run the scripts for actual processing (with ALOS-1 data as an example), we need to put two unzipped ALOS-1 data folders (with the folder name formatted as "ALPSRP*-L1.0") in the same directory, e.g. test_data. For running insarApp, one only needs to type the following command line:
	
	single_scene_insarApp.py -f test_data

and for running stripmapApp, one can type:

	single_scene_stripmapApp.py -f test_data

***Note: some of the parameters in the 7 scripts of 0) are hardcoded for the ALOS data as an example of using the scripts, and needs to be adjusted for ALOS-2 and the future NISAR data.***

***Note: for better use of updated functions and also to be compatible with future ISCE releases, it is thus recommended not to simply replace those ISCE original files in 1-5) but to directly add the newly added lines into the ISCE original files. Those newly added lines start and end with the pattern shown below:***

    # NEW COMMANDS added by YL --start
    	...
    # NEW COMMANDS added by YL --end

---------------------------------------------------------------------------------------------------

## Steps 2 and 3, if using ROI_PAC:

In step 2 and step 3, for ROI_PAC-processed results, run the following command line:

	python directory_of_scripts/CROP_ROIPAC.py dirname date1 date2

	dirname	-	the directory where the ROI_PAC amp/cor files are located
	date1	-	date for 1st SAR acquisition
	date2	-	date for 2nd SAR acquisition

for cropping the image margin and refer to online ROI_PAC guidance for the geocoding command "geocode.pl" (not included here). 

## Steps 2 and 3, if using ISCE: these steps had already been incorporated in the workflow.

***Note: the amount of margin to be cropped are hardcoded based on the ALOS SAR image dimension, and needs to be adjusted for ALOS-2 and the future NISAR image.***
