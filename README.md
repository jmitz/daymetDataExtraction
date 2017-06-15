# Daymet Data Download
### Purpose
Script to download [Daymet](https://daymet.ornl.gov/) climatalogical data.
<<<<<<< HEAD
=======

Script to extract climate data for the Greater Yellowstone Area (GYA) from the Daymet rasters. (Actually this script will extract data for any raster mask )

This was based on work done by Mike Tercek (miketercek@yahoo.com) The file structure of the CSV files integrate with extraction and analysis tools developed for the Yellowstone Center for Resources, Yellowstone National Park.
>>>>>>> master

Script to extract climate data for the Greater Yellowstone Area (GYA) from the Daymet rasters. (Actually this script will extract data for any raster mask )

This was based on work done by Mike Tercek (miketercek@yahoo.com) The file structure of the CSV files integrate with extraction and analysis tools developed for the Yellowstone Center for Resources, Yellowstone National Park.

### Requirements
The scripts have been written to run under Python 3.6.0. In particular I installed [Anaconda](https://www.continuum.io/anaconda-overview) and documented the use of the script with Jupyter Notebook.

One note that should be made is that when using Python 3.6.0 and Anaconda on Windows, the GDAL library needs to be set up for Windows. The normal library that is downloaded with conda does not work properly. I downloaded GDAL from should be downloaded from Chrostoph Gohlke's [Unofficial Windows Binaries for Python Extension Packages](http://www.lfd.uci.edu/~gohlke/pythonlibs/)

### Starting the Jupyter Notebook
- Clone the repository.
- Ensure that jupyter has been installed (Anaconda automatically installs jupyter)
- Change directory into the project directory
- Type <code>jupyter notebook</code> at the command prompt
- Web browser should open up to the jupyter page.
- Click on daymetDataDownload.ipynb

