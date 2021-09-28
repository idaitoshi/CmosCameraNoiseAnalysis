"""

===========================================
CMOS camera noise analysis program ver.1.0
===========================================

*By: so-nano-car inspired by Mr. "Apranat"*
*Original source code URL:https://so-nano-car.com/noise-evaluation-of-qhy5iii174m
*Arrange: Daitoshi 

*License: BSD*

*プログラムの使用方法*
コマンドライン引数を指定しない場合は、実行されたカレントディレクトリのサブディレクトリ./fits/ 以下の*.fitsファイルを処理対象とします
一つ目の引数は、fitsファイルのパスとして解釈される パスの最後の文字は \ or / では無い状態で指定すること 例 c:\hoge\fits
二つ目の引数は、グラフのタイトルとして解釈される 空白文字は入れずに、_ で代用すること 例 ASI294_Dark_gain300_30c*128files
コマンドライン例 
python fitsAnalayze.py "C:\home\SharpCap Captures\2021-09-26\Capture\Dark" ASI294_Dark_gain300_30c*128files
"""

import matplotlib.pyplot as plt
import numpy as np
import glob
from astropy.visualization import astropy_mpl_style
from astropy.io import fits
import time
import sys

# Load sensor pixel size (array size)
def getSenserPixelSize(fitspath):
    imdata = fits.getdata(glob.glob(fitspath)[0], ext = 0) # Get the x,y size of the first fits file found.
    array_y = np.shape(imdata)[0]
    array_x = np.shape(imdata)[1]
    return(array_x, array_y)

# Load files and number of files: n, then store to 3-D numpy array
def loadFilesStore3DnumpyArray(fitspath, array_x, array_y, fileLoadLimit=99999):
    stack = np.empty((0, array_y, array_x))
    fitsFiles = glob.glob (fitspath)
    fitsNum   = len(fitsFiles)
    for i, img in enumerate(fitsFiles):
        readNum = i+1
        imdata = fits.getdata(img, ext = 0)
        stack = np.append(stack, imdata[np.newaxis,:], axis = 0)
        print(f"loadFitsFiles {readNum}/{fitsNum}")
        if(fileLoadLimit <= readNum): # ファイル数読み込みの上限を超えていたらそこで処理打ち切り
            print(f"fileLoadLimit=={fileLoadLimit}")
            break
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
def plotResults(x, y, title):
    plt.style.use(astropy_mpl_style)
    plt.scatter(x, y, s = 0.3, marker = '.', color = "blue")
    plt.grid(which = "both", linewidth = 0.5, alpha = 0.1)
    plt.suptitle(title)
    plt.xlabel('Median')
    plt.ylabel('Std.dev.')
    plt.xscale("log")
    plt.yscale("log")
    plt.xlim([100,100_000])
    plt.ylim([10,100_000])
    plt.show()

# Main routine
if __name__ == '__main__':
    # デフォルトパラメータの設定
    DEFAULT_LOAD_FITS_PATH = './fits/*.fits'
    DEFAULT_SAVE_CSV_NAME  = './fits/result.csv'
    DEFAULT_TITLE          = "Bias"
    FILE_LOAD_LIMIT        = 32
    load_fits_path = DEFAULT_LOAD_FITS_PATH
    save_csv_path  = DEFAULT_SAVE_CSV_NAME
    title = DEFAULT_TITLE
    CsvExportFlag = False # If CsvExportFlag is True, output a csv file.

    # コマンドライン引数の処理
    args = sys.argv
    if(2 <= len(args)):
        load_fits_path = args[1] + '/*.fits'
    if(3 <= len(args)):
        title = args[2]

    # Check for the existence of fits files
    if(len(glob.glob(load_fits_path)) == 0):
        print(f"Exit the program because the fits file does not exist. => {load_fits_path}")
        exit()

    # Load start time
    startTime = time.time()

    # Load Fits and Store data
    array_x, array_y = getSenserPixelSize(load_fits_path)
    stack = loadFilesStore3DnumpyArray(load_fits_path , array_x, array_y, FILE_LOAD_LIMIT)
    print(f'{np.shape(stack)[0]} files loaded.')
    print(f'Elapsed time ={time.time() - startTime} s.')

    # Calculate Ploting Point
    x,y = calculatePlotingPoint(stack, array_x, array_y)
    # Calculate elapsed time
    print(f'Elapsed time ={time.time() - startTime} s.')

    # CsvExport
    if(CsvExportFlag):
        exportToCsvFile(x,y, save_csv_path)

    # Plot
    plotResults(x,y,title)
