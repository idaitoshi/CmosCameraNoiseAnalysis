"""

===========================================
CMOS camera noise analysis program ver.1.0
===========================================

*By: so-nano-car inspired by Mr. "Apranat"*
*Original source code URL:https://so-nano-car.com/noise-evaluation-of-qhy5iii174m
*Arrange: Daitoshi 

*License: BSD*

"""

import matplotlib.pyplot as plt
import numpy as np
import glob
from astropy.visualization import astropy_mpl_style
from astropy.io import fits
import time

# Load sensor pixel size (array size)
def getSenserPixelSize(fitspath):
    imdata = fits.getdata(glob.glob(fitspath)[0], ext = 0) # Get the x,y size of the first fits file found.
    array_y = np.shape(imdata)[0]
    array_x = np.shape(imdata)[1]
    return(array_x, array_y)

# Load files and number of files: n, then store to 3-D numpy array
def loadFilesStore3DnumpyArray(fitspath, array_x, array_y):
    stack = np.empty((0, array_y, array_x))
    for img in glob.glob (fitspath):
        imdata = fits.getdata(img, ext = 0)
        stack = np.append(stack, imdata[np.newaxis,:], axis = 0)
    return(stack)

# Calculate x,y
def calculatePlotingPoint(stack, array_x, array_y):
    # Calculate median and std.dev. of each pixel
    median = np.median(stack, axis = 0)
    stddev = np.std(stack, axis = 0,ddof = 0)

    # Reshape median and std.dev. array for plotting
    x = median.reshape([array_y * array_x,1])
    y = stddev.reshape([array_y * array_x,1])
    return(x,y)

# Export to csv file
def exportToCsvFile(x,y,saveCsvname):
    data = np.concatenate([x, y], 1)
    np.savetxt(saveCsvname, data, delimiter = ',')

# Plot results
def plotResults(x, y):
    plt.style.use(astropy_mpl_style)
    plt.scatter(x, y, s = 0.3, marker = '.', color = "blue")
    plt.grid(which = "both", linewidth = 0.5, alpha = 0.1)
    plt.suptitle("Bias")
    plt.xlabel('Median')
    plt.ylabel('Std.dev.')
    plt.xscale("log")
    plt.yscale("log")
    plt.xlim([100,100_000])
    plt.ylim([10,100_000])
    plt.show()

# Main routine
if __name__ == '__main__':
    LOAD_FITS_PATH = './fits/*.fits'
    SAVE_CSV_NAME  = './result.csv'
    CsvExportFlag = False # If CsvExportFlag is True, output a csv file.

    # Check for the existence of fits files
    if(len(glob.glob(LOAD_FITS_PATH)) == 0):
        print(f"Exit the program because the fits file does not exist. => {LOAD_FITS_PATH}")
        exit()

    # Load start time
    startTime = time.time()

    # Load Fits and Store data
    array_x, array_y = getSenserPixelSize(LOAD_FITS_PATH)
    stack = loadFilesStore3DnumpyArray(LOAD_FITS_PATH , array_x, array_y)
    print(f'{np.shape(stack)[0]} files loaded.')

    # Calculate Ploting Point
    x,y = calculatePlotingPoint(stack, array_x, array_y)
    # Calculate elapsed time
    print(f'Elapsed time ={time.time() - startTime} s.')

    # CsvExport
    if(CsvExportFlag):
        exportToCsvFile(x,y, SAVE_CSV_NAME)

    # Plot
    plotResults(x,y)
