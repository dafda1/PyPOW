# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 09:36:12 2024

@author: dafda1
"""

# import modules / functions
import numpy as np
import matplotlib.pyplot as plt
from PyPOW.import_module import import_xrdml_data

#%% import data from XRDML file
df, meta = import_xrdml_data("ASG1_1.XRDML", include_metadata = True)

#%% plot data from XRDML file
# in this example in 2theta as well as d-spacing

fig, axes = plt.subplots(nrows = 2, figsize = (2*6.4, 1.5*4.8))

ax = axes[0] #2theta plot

ax.errorbar(df["2Theta (deg)"], df["Intensity (counts)"],
            yerr = df["Intensity ESD (counts)"])

ax.set_xlabel(r"2$\Theta$ (deg)")
ax.set_xlim(5, 90)

ax.set_ylabel("Intensity (counts)")
ax.set_ylim(0, None)

ax = axes[1] #dspacing plot

ax.errorbar(df["d-spacing (Angstrom)"], df["Intensity (counts)"],
            yerr = df["Intensity ESD (counts)"])

ax.set_xlabel(r"$d-$spacing ($\AA$)")
ax.set_xlim(np.min(df["d-spacing (Angstrom)"]), 6.5)

ax.set_ylabel("Intensity (counts)")
ax.set_ylim(0, None)

plt.tight_layout()

#%% change data formating to XY file and export it using numpy
# in this example using 2theta as the x-axis coordinate and without errorbars
# and we include wavelength info in header

from PyPOW.import_module import extract_intended_wavelength as get_wvl

data = np.empty((df.index.size, 2), dtype = float)
data[:, 0] = df["2Theta (deg)"]
data[:, 1] = df["Intensity (counts)"]

np.savetxt("ASG_1_edited.xy", data, fmt = ("%.3f", "%.1f"),
           header = "lambda = %.5f %s\n" % get_wvl(meta['usedWavelength']) +\
                    "2theta (deg), Intensity (counts)")