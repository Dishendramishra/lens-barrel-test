#%%

import numpy as np 
import matplotlib.pyplot as plt
from scipy.ndimage.filters import uniform_filter1d
from astropy.io import fits
import glob
import os

def mean(pixel_arrays):
    # input :  [a1,a2,a3]
    # output:  2D matrix having pixel-wise mean values    

    return np.mean(pixel_arrays,axis=0)

def median(pixel_arrays):
    # input :  [a1,a2,a3]
    # output:  2D matrix having pixel-wise median values    

    return np.median(np.dstack(pixel_arrays),-1)

def read_fits(filename):
    # input :   string filename to be read
    # output:   pixel array

    return fits.getdata(filename)

def write_fits(filename, data):
    # input:- 
    #   filename: string 
    #   data    : pixel array

    try:
        fits.writeto(filename,data)
    except:
        fits.writeto("new_"+filename,data)

def combine_frames(filenames,avg_type="mean"):
    frames = []
    for i in filenames:
        frames.append(np.genfromtxt(i,skip_header=14))

    if avg_type == "median":
        return median(frames)
    else:
        return mean(frames)

def remove_latex(s):

    for i in ['frac','\\','$','}{',"{",'}']:
        if i == '}{':
            s = s.replace(i,"_")
        else:
            s = s.replace(i,"")
    
    return s

def plot(x,y,limits=None,title=None):
    plt.figure(figsize=(19.20,10.80))
    if limits:
        plt.axis(limits)
    if title:
        plt.title(title, fontsize=20)
    # wm = plt.get_current_fig_manager()
    # wm.window.showMaximized()
    plt.locator_params(nbins=50)
    plt.tight_layout()
    plt.grid(True)
    plt.plot(x,y)
    plt.savefig(remove_latex(title)+".png",dpi=300)
    # plt.show()  

#%%

# Working Directory
path = "22-02-2021"
os.chdir(path)

# Gettings Filenames
darks_filenames     = glob.glob("dark*.txt")
filter_1_filenames  = glob.glob("filter (*.txt")
filter_2_filenames  = glob.glob("filter_2*.txt")
lens_filenames      = glob.glob("lens*.txt")
ref_filenames       = glob.glob("ref*.txt")

#  Combing frames
darks       = combine_frames(darks_filenames,avg_type="median")
filter_1    = combine_frames(filter_1_filenames,avg_type="median")
filter_2    = combine_frames(filter_2_filenames,avg_type="median")
lens        = combine_frames(lens_filenames,avg_type="median")
ref         = combine_frames(ref_filenames,avg_type="median")

#  Taking Moving Average of the combined frames
darks[:,1]      = uniform_filter1d(darks[:,1],size=3)
filter_1[:,1]   = uniform_filter1d(filter_1[:,1],size=3)
filter_2[:,1]   = uniform_filter1d(filter_2[:,1],size=3)
lens[:,1]       = uniform_filter1d(lens[:,1],size=3)
ref[:,1]        = uniform_filter1d(ref[:,1],size=3)

# Subtracting Darks
lens[:,1]       = lens[:,1] - darks[:,1]
ref[:,1]        = ref[:,1] - darks[:,1]
filter_1[:,1]   = filter_1[:,1] - darks[:,1]
filter_2[:,1]   = filter_2[:,1] - darks[:,1]


lens_by_ref = lens[:,1]/ref[:,1]


plot(lens[:,0],lens_by_ref,[400,700,0,2],title=r'$\frac{LensBarrel}{Ref}$')
plot(lens[:,0],ref[:,1],[400,700,2000,13500],title="Ref")
plot(lens[:,0],lens[:,1],[400,700,2000,13500],title="Lens Barrel")
plot(lens[:,0],filter_1[:,1],[400,700,None,None],title="Filter_1")
plot(lens[:,0],filter_2[:,1],[400,700,None,None],title="Filter_2")


