# 2.1 Generate interferograms

The preprocessing [scripts](https://github.com/leiyangleon/FSH/blob/dev/ISCE_processing_scripts) first need to be set up properly, which is done once and for all. After setting up these scripts, there are three steps for the preprocessing, which has been simplified as easy as 1 command line for using ISCE. 

## 2.1.1 Preparation
## 2.1.2 Run ROI_PAC/ISCE (Step I)
## 2.1.3 Crop the image margin of ROI_PAC/ISCE output (Step II)
## 2.1.4 Geocode the ROI_PAC/ISCE output (Step III)

=====================================================================================


## 2.1.1 Preparation

Users may find online support and guidance running ROI_PAC (the command "process_2pass.pl"). Since it only supports ALOS-1 data and has been deprecated, we do not cover the details for running it. Instead, we provide the details along with the scripts for running ISCE, with the precursor being ROI_PAC. ISCE supports JAXA's ALOS-1 and ALOS-2 data and also NASA's future NISAR mission. ISCE's application "insarApp.py" is valid for ISCE v2.0, v2.1 and v2.2, while deprecated for v2.3. "insarApp.py" uses the amplitude cross-correlation (ampcor) to coregister the two radar images. In contrast, starting from v2.2, ISCE started to replace the role of "insarApp.py" with "stripmapApp.py", which uses the radar observing geometry along with dense ampcor + rubbersheeting (to apply the ampcor-determined offsets) for image coregistration. As each method has its own merit, and so far neither is absolutely better than the other for our application, we include both options and leave the quality assessment to the users. Since ISCE v2.2 is the only version of ISCE that supports both "insarApp.py" and "stripmapApp.py", we provide the preprocessing scripts for this version ([ISCE v2.2.0](https://github.com/leiyangleon/FSH/blob/dev/ISCE_processing_scripts/ISCE_v2.2.0)). Recently, "stripmapApp.py" has been upgraded by including rubbersheeting in range direction in the latest ISCE versions (e.g. v2.4+). Therefore, we also provide the preprocessing scripts ("stripmapApp.py" only) for this version ([ISCE v2.4.1](https://github.com/leiyangleon/FSH/blob/dev/ISCE_processing_scripts/ISCE_v2.4.1)). However, the scripts are meant to work with all other versions of ISCE v2, with little modifications if necessary. 

***Note we have also provided the ALOS-2 support in the current release of our preprocessing scripts. Users would only need to set up the scripts as instructed below and run the exact same command for either ALOS-1 or ALOS-2 data. The scripts are wise enough to determine which sensor the data were acquired from and then pick up the proper internal processing routine of ISCE.***

All the ISCE preprocessing scripts can be found under the [folder](https://github.com/leiyangleon/FSH/blob/dev/ISCE_processing_scripts).
Below are the steps we set up the updated ISCE applications (that requires replacing existing ISCE scripts) "insarApp" and "stripmapApp" to process radar (e.g. ALOS PALSAR in the test examples) data for FSH.

***For [ISCE v2.2.0](https://github.com/leiyangleon/FSH/blob/dev/ISCE_processing_scripts/ISCE_v2.2.0)***

- Copy updated applications scripts,

      0) Copy the 7 scripts (CROP_ISCE_insarApp.py, CROP_ISCE_stripmapApp.py, format_insarApp_xml.py, \
      format_stripmapApp_xml.py, MULTILOOK_FILTER_ISCE.py, single_scene_insarApp.py, \
      single_scene_stripmapApp.py) under "ISCE_processing_scripts/ISCE_v2.2.0/" to any local folder that is \
      on the environmental variables PATH and PYTHONPATH

- For using ISCE's insarApp, 

      1) Replace ISCE/isce/components/isceobj/InsarProc/runCoherence.py with \
      ISCE_processing_scripts/ISCE_v2.2.0/insarApp_substitute/runCoherence.py
	
- For using ISCE's stripmapApp,

      2) Replace ISCE/isce/components/isceobj/StripmapProc/runCoherence.py with \
      ISCE_processing_scripts/ISCE_v2.2.0/stripmapApp_substitute/runCoherence.py

      3) Replace ISCE/isce/components/isceobj/StripmapProc/runGeocode.py with \
      ISCE_processing_scripts/ISCE_v2.2.0/stripmapApp_substitute/runGeocode.py

      4) Replace ISCE/isce/components/isceobj/StripmapProc/runPreprocessor.py with \
      ISCE_processing_scripts/ISCE_v2.2.0/stripmapApp_substitute/runPreprocessor.py

      5) Replace ISCE/isce/applications/stripmapApp.py with \
      ISCE_processing_scripts/ISCE_v2.2.0/stripmapApp_substitute/stripmapApp.py

***For [ISCE v2.4.1](https://github.com/leiyangleon/FSH/blob/dev/ISCE_processing_scripts/ISCE_v2.4.1)***

- Copy updated applications scripts,

      0) Copy the 4 scripts (CROP_ISCE_stripmapApp.py, format_stripmapApp_xml.py, \
      MULTILOOK_FILTER_ISCE.py, single_scene_stripmapApp.py) under \
      "ISCE_processing_scripts/ISCE_v2.4.1/" to any local folder that is \
      on the environmental variables PATH and PYTHONPATH

- For using ISCE's stripmapApp,

      1) Replace ISCE/isce/components/isceobj/StripmapProc/runCoherence.py with \
      ISCE_processing_scripts/ISCE_v2.4.1/stripmapApp_substitute/runCoherence.py

      2) Replace ISCE/isce/components/isceobj/StripmapProc/runGeocode.py with \
      ISCE_processing_scripts/ISCE_v2.4.1/stripmapApp_substitute/runGeocode.py
      
      3) Replace ISCE/isce/components/isceobj/StripmapProc/runInterferogram.py with \
      ISCE_processing_scripts/ISCE_v2.4.1/stripmapApp_substitute/runInterferogram.py

      4) Replace ISCE/isce/components/isceobj/StripmapProc/runPreprocessor.py with \
      ISCE_processing_scripts/ISCE_v2.4.1/stripmapApp_substitute/runPreprocessor.py

      5) Replace ISCE/isce/applications/stripmapApp.py with \
      ISCE_processing_scripts/ISCE_v2.4.1/stripmapApp_substitute/stripmapApp.py


## 2.1.2 Run ROI_PAC/ISCE (Step I)

To run the scripts for actual processing (with ALOS-1/-2 data as an example), we need to put two unzipped ALOS-1/-2 data folders (with the folder name formatted as "ALPSRP*-L1.0" for ALOS-1 and "* _ALOS2 *" for ALOS-2) in the same directory, say "test_data". For running insarApp ([ISCE v2.2.0](https://github.com/leiyangleon/FSH/blob/dev/ISCE_processing_scripts/ISCE_v2.2.0)), one only needs to type the following command line:
	
    single_scene_insarApp.py -f test_data

and for running stripmapApp ([ISCE v2.2.0](https://github.com/leiyangleon/FSH/blob/dev/ISCE_processing_scripts/ISCE_v2.2.0) and [ISCE v2.4.1](https://github.com/leiyangleon/FSH/blob/dev/ISCE_processing_scripts/ISCE_v2.4.1)), one can type:

    single_scene_stripmapApp.py -f test_data

***Note: some of the parameters in the 7 scripts are hardcoded for the ALOS-1/-2 data as an example of using the scripts, and need to be adjusted for other sensors, e.g. the future NISAR data.***

***Note: for better use of updated functions and also to be compatible with other ISCE releases, it is thus recommended not to simply replace those ISCE original files in 1-5) but to directly add the newly added lines into the ISCE original files. Those newly added lines start and end with the pattern shown below:***

    # NEW COMMANDS added by YL --start
    	...
    # NEW COMMANDS added by YL --end

***Note: there is only 1 command line involved for the actual processing using either insarApp or stripmapApp of ISCE after the above preparation, which is done once and for all.***

---------------------------------------------------------------------------------------------------

## 2.1.3 Crop the image margin of ROI_PAC/ISCE output (Step II)
## 2.1.4 Geocode the ROI_PAC/ISCE output (Step III)

If using [ISCE preprocessing scripts](https://github.com/leiyangleon/FSH/blob/dev/ISCE_processing_scripts) provided, these steps had already been incorporated in the workflow of Step I (can skip this).

While using ROI_PAC, the image margin of the ROI_PAC-processed results can be cropped by running the following command line:

	python CROP_ROIPAC.py dirname date1 date2

	dirname	-	the directory where the ROI_PAC amp/cor files are located
	date1	-	date for 1st SAR acquisition
	date2	-	date for 2nd SAR acquisition

and refer to online ROI_PAC guidance for the geocoding command "geocode.pl" (not included here). 


***Note: the amount of margin to be cropped are hardcoded based on the ALOS-1/-2 SAR image dimension, and needs to be adjusted for other sensors, e.g. the future NISAR image.***
