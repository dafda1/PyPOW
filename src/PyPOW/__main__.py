# -*- coding: utf-8 -*-
"""
Created on Mon Jun  2 16:15:13 2025

@author: dafda1
"""

# import modules / functions
import numpy as np

from PyPOW.import_module import import_xrdml_data
from PyPOW.import_module import extract_intended_wavelength as get_wvl

import sys

#%% define conversion functions

def change_file_extension (filename):
    return filename[:-5] + "xy"

def convert_file (filename):
    df, meta = import_xrdml_data(filename, include_metadata = True)
    newfile = change_file_extension(filename)

    #initialise data array and write 2 theta and intensity columns
    data = np.empty((df.index.size, 2), dtype = float)
    data[:, 0] = df["2Theta (deg)"]
    data[:, 1] = df["Intensity (counts)"]

    #save as text (xy) file
    np.savetxt(newfile, data, fmt = ("%.3f", "%.1f"),
               header = "wavelength = %.5f %s\n" % get_wvl(meta['usedWavelength']) +\
                        "2theta (deg), Intensity (counts)")

    #save dataframe as csv
    df.to_csv(filename[:-5] + "csv")
    return newfile

#%% run conversions
def convert_files():

    if len(sys.argv) < 2:
        raise ValueError("Must specify filenames to convert.")
    else:
        files_to_convert = sys.argv[1:]

    for filename in files_to_convert:
        print(f">> Converting file {filename}.")
        newfile = convert_file(filename)
        print(f" >> Done. Created file {newfile}.")

if __name__ == "__main__":
    convert_files()
