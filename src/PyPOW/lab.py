# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 10:53:05 2024

@author: dafda1
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from xmltodict import parse

#%%

def read_quantity_w_units (key, dictionary):
    obj = dictionary[key]
    unit = obj["@unit"]
    text = obj["#text"]
    return f"{key} = {text} {unit}"

def check_if_quantity (key, dictionary):
    obj = dictionary[key]
    if type(obj) == dict:
        if "@unit" in obj.keys() and "@unit" in obj.keys():
            return True
        else:
            return False
    else:
        return False

#%%

with open("ASG1_1.XRDML", "rb") as fp:
    # print(fp.readlines())
    data_xrdml = parse(fp)

fp.close()
del fp

#%%

"""
need the values associated with the keywords 'startPosition' and 'endPosition'
somewhere in there and then the number of intensities should tell me what the
delta-2theta is based on those
N = #num intensities
i=0 -> 2theta = startPosition
i=N-1 -> 2theta = endPosition
2theta_values = np.linspace(startPosition, endPosition, N)
"""

new_data = data_xrdml["xrdMeasurements"]["xrdMeasurement"]["scan"]["dataPoints"]

count_time = new_data["commonCountingTime"]
intensities = new_data["intensities"]
positions = new_data["positions"]

wavelength_val = float(data_xrdml["xrdMeasurements"]["xrdMeasurement"]["usedWavelength"]["kAlpha1"]["#text"])

twotheta_start = float(positions["startPosition"])
twotheta_end = float(positions["endPosition"])

intensity_vals = np.array(intensities["#text"].split(), dtype = int)

twotheta_vals = np.linspace(twotheta_start, twotheta_end, intensity_vals.size)

fig, axes = plt.subplots(nrows = 3, figsize = (2*6.4, 3*4.8))

ax = axes[0]

ax.errorbar(twotheta_vals, intensity_vals, yerr = np.sqrt(intensity_vals))

ax.set_xlabel(r"2$\theta$ (deg)")
ax.set_xlim(twotheta_start, twotheta_end)
ax.set_ylabel("Intensity (counts)")

ax = axes[1]

dspacing_vals = wavelength_val*1.0/(2*np.sin(twotheta_vals*np.pi/360.0))

ax.errorbar(dspacing_vals, intensity_vals, yerr = np.sqrt(intensity_vals))

ax.set_xlabel(r"$d$ ($\AA$)")
ax.set_xlim(np.min(dspacing_vals), np.max(dspacing_vals))
ax.set_ylabel("Intensity (counts)")

ax = axes[2]

Q_vals = 2*np.pi/dspacing_vals

ax.errorbar(Q_vals, intensity_vals, yerr = np.sqrt(intensity_vals))

ax.set_xlabel(r"$Q$ ($\AA^{-1}$)")
ax.set_xlim(np.min(Q_vals), np.max(Q_vals))
ax.set_ylabel("Intensity (counts)")

plt.tight_layout()

#%%

df = pd.DataFrame(columns = ("2theta (deg)", "d-spacing (Ang)",
                             "Q (invAng)", "Intensity (counts)",
                             "Intensity_sig (counts)"),
                  dtype = float)

df["2theta (deg)"] = twotheta_vals
df["d-spacing (Ang)"] = dspacing_vals
df["Q (invAng)"] = Q_vals
df["Intensity (counts)"] = intensity_vals
df["Intensity_sig (counts)"] = np.sqrt(intensity_vals)

df.to_csv("ASG1_1.csv")