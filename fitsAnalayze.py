"""

===========================================
CMOS camera noise analysis program ver.1.0
===========================================

*By: so-nano-car inspired by Mr. "Apranat"*

*License: BSD*

"""

import matplotlib.pyplot as plt
from matplotlib.pyplot import axis
import numpy as np
#import pandas as pd
import glob
#import astropy
import numpy as np
from astropy.visualization import astropy_mpl_style
from numpy.core.fromnumeric import shape, std
plt.style.use(astropy_mpl_style)
from astropy.utils.data import get_pkg_data_filename
from astropy.io import fits
import time

# Load start time
t1 = time.time()

# Load sensor pixel size (array size)
for img in glob.glob ('./fits/*.fits'):
    imdata = fits.getdata(img, ext = 0)
array_y = np.shape(imdata)[0]
array_x = np.shape(imdata)[1]

# Load files and number of files: n, then store to 3-D numpy array
stack = np.empty((0,array_y,array_x))
for img in glob.glob ('./fits/*.fits'):
    imdata = fits.getdata(img, ext = 0)
    stack = np.append(stack,imdata[np.newaxis,:],axis = 0)
count = np.shape(stack)[0]
print('{0} files loaded.'.format(count))

# Calculate median and std.dev. of each pixel
median = np.median(stack, axis = 0)
stddev = np.std(stack, axis = 0,ddof = 0)

# Reshape median and std.dev. array for plotting
x = median.reshape([array_y * array_x,1])
y = stddev.reshape([array_y * array_x,1])

# Export to csv file
data = np.concatenate([x,y], 1)
np.savetxt('./fits/result.csv',data,delimiter = ',')

# Calculate elapsed time
t2 = time.time()
elapsed_time = t2 - t1
print("Elapsed time ={0} s.".format(elapsed_time))

# Plot results
plt.scatter(x,y,s = 0.3, marker = '.', color = "blue")
plt.grid(which = "both", linewidth = 0.5, alpha = 0.1)
plt.suptitle("Bias")
plt.xlabel('Median')
plt.ylabel('Std.dev.')
plt.xscale("log")
plt.yscale("log")
plt.xlim([100,100000])
plt.ylim([10,100000])
plt.show()
