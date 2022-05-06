#!/usr/bin/python

import os
import pandas as pd
import numpy as np
import geopy.distance
pd.options.mode.chained_assignment = None  # default='warn'
pd.options.mode.use_inf_as_na = True

# set directories and files
cwd = os.getcwd()
input_folder = "0_input"

# import files
df = pd.read_excel(os.path.join(cwd,"GPS_input.xlsx"))
df['Latitude'] = df['Latitude'].astype('float')
df['Longitude'] = df['Longitude'].astype('float')
df['3miles'] = 0

# √[(x₂ - x₁)² + (y₂ - y₁)²]
for i in range(0, df.index[-1]):
    lat_i = df['Latitude'][i]
    lon_i = df['Longitude'][i]
    coords_1 = (lat_i, lon_i)

    for j in range(0, df.index[-1]):
        lat_j = df['Latitude'][j]
        lon_j = df['Longitude'][j]
        coords_2 = (lat_j, lon_j)

        if df['Company'][i] != df['Company'][j]: # company1 not equal company2
            dist_km = geopy.distance.geodesic(coords_1, coords_2).km
            if dist_km <= 4.82:
                #4.82km = 3 miles
                df['3miles'][i] = 1
                print( df['Company'][i], '   /   ', df['Company'][j], '   /   '
                       , coords_1, coords_2, '   /   ',dist_km)
            else:
                pass
        else:
            pass

df = df[df['3miles'] == 1]
# export
df.to_excel(os.path.join(cwd,"gps_output_2_clusters.xlsx"), index=False)
#print(df)