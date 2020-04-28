# I. Required software packages and installation

To run these python scripts the following software packages are needed:

Python (This code was developed and tested using Version 2.7 and has been updated to Version 3.6+)
These python libraries: NumPy, SciPy, SimPy, json, pillow, OsGeo/GDAL, simplekml, mpmath

## Recommendations for installing on OSX, Linux, Windows systems

- For Mac/Linux users: libraries can be installed with pip. Alternatively one may use MacPorts (https://www.macports.org/) to install Python along with the above libraries.

- For Windows users: it is recommend to use the Anaconda distribution of python, as it is designed for scientific computing, and comes with Numpy, SciPy, json, and pillow.

- If needed, one can obtain the simplekml package at www.simplekml.com (follow the download links to https://pypi.python.org/pypi/simplekml). 

- If needed, the OsGeo/GDAL can be installed on Windows using the following steps
	
      1) Download and install Microsoft Visual C++ for the Windows version you have.
      2) Go to http://www.gisinternals.com/release.php and click on the link corresponding to your MSVC version and Windows 32/64 bit version
      3) From the link above Download and install the 'gdal-111-1400-core.msi' and 'GDAL-1.11.1.win32-py2.7.msi' (or whatever verion of python you have, eg py3.3)
      4) From the link above Download and extract the dir 'release-1600-gdal-1-11-1-mapserver-6-4-1'
      5) Once the dir is unzipped, copy all files in dir bin/gdal/python/* to C:\Users\keb\Anaconda\Lib\site-packages\ (or the site-packages directory of whatever python distribution you are using)
      6) Add 'Program Files/GDAL' to the system PATH variable (NOT the user PATH variable) in system settings (thru control panel > advanced settings)
      7) To test if everything is installed correctly:
        at the cmd prompt (cmd.exe) type 'gdalinfo -h' and you should get some options such as -stats etc 
        in python type 'from osgeo import gdal' and you shouldn't get an error.
