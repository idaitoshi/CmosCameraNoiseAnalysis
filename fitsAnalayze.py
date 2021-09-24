"""

===========================================
CMOS camera noise analysis program ver.1.0
===========================================

*By: so-nano-car inspired by Mr. "Apranat"*
*Arrange: Daitoshi

*License: BSD*

"""

import matplotlib.pyplot as plt
from matplotlib.pyplot import axis
import numpy as np
import glob
import numpy as np
from astropy.visualization import astropy_mpl_style
from numpy.core.fromnumeric import shape, std
from astropy.utils.data import get_pkg_data_filename
from astropy.io import fits
import time

# Load sensor pixel size (array size)
def getSenserPixelSize(fitspath):
    for img in glob.glob (fitspath):
        imdata = fits.getdata(img, ext = 0)
    array_y = np.shape(imdata)[0]
    array_x = np.shape(imdata)[1]
    return(array_x, array_y)

# Load files and number of files: n, then store to 3-D numpy array
def loadFilesStore3DnumpyArray(fitspath, array_x,array_y):
    stack = np.empty((0,array_y,array_x))
    for img in glob.glob (fitspath):
        imdata = fits.getdata(img, ext = 0)
        stack = np.append(stack,imdata[np.newaxis,:],axis = 0)
    return(stack)

# Calculate x,y
def calculatePlotingPoint(stack):
    # Calculate median and std.dev. of each pixel
    median = np.median(stack, axis = 0)
    stddev = np.std(stack, axis = 0,ddof = 0)

    # Reshape median and std.dev. array for plotting
    x = median.reshape([array_y * array_x,1])
    y = stddev.reshape([array_y * array_x,1])
    return(x,y)

# Export to csv file
def exportToCsvFile(x,y,saveCsvname):
    data = np.concatenate([x,y], 1)
    np.savetxt(saveCsvname,data,delimiter = ',')


# Plot results
def plotResults(x,y):
    plt.style.use(astropy_mpl_style)
    plt.scatter(x,y,s = 0.3, marker = '.', color = "blue")
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

    # Load start time
    startTime = time.time()

    array_x, array_y = getSenserPixelSize(LOAD_FITS_PATH)
    stack = loadFilesStore3DnumpyArray(LOAD_FITS_PATH , array_x, array_y)
    print(f'{np.shape(stack)[0]} files loaded.')

    x,y = calculatePlotingPoint(stack)
    # Calculate elapsed time
    print(f'Elapsed time ={time.time() - startTime} s.')

    exportToCsvFile(x,y, SAVE_CSV_NAME)

    plotResults(x,y)
