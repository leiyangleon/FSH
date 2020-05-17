- **In a future release of the software, backscatter-inverted mosaic map will also be incorporated to this InSAR coherence-based mosaic map to generate a final mosaic of FSH (see the [citation](https://ieeexplore.ieee.org/document/8439086)).**

- **Preprocessing scripts (in the folder [ISCE_processing_scripts](https://github.com/leiyangleon/FSH/tree/dev/ISCE_processing_scripts)) have been added for using ISCE's insarApp (up to v2.2) and stripmapApp (v2.2+) with only 1 command line for actual data processing after appropriate setup. Test examples of using insarApp and stripmapApp are provided as well. All the [historial ISCE versions](https://winsar.unavco.org/software/isce) and the [current ISCE version](https://github.com/isce-framework/isce2) can be used to process ALOS-1 and ALOS-2 stripmap InSAR data.** *[update: March 28, 2020]*

- **The Python 3 scripts are ready to use. Please use the folder [scripts_Py3](https://github.com/leiyangleon/FSH/tree/dev/scripts_Py3) instead of the one using Python 2 ([scripts](https://github.com/leiyangleon/FSH/tree/dev/scripts)). This Python 3 version of the scripts can be run the same as the Python 2 version (replacing "python" in all the following commands with "python3"), or can run in Google Colaboratory (with unix operating system) using [Exercise_1_FSH on the SERVIR Global GitHub](https://github.com/SERVIR/ForestStandHeight).** *[update: January 16, 2020]*

- **Only 2 command lines are involved to automatically perform the forest height inversion and mosaicking task (1 command for FSH inversion and 1 for FSH mosaicking).** *[update: June 29, 2017]*


