#!/usr/bin/env python

# Author: Duncan Law-Green (dlg@kyubi.co.uk)
# Copyright 2017 Kyubi Systems
# 
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
# 
#    http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# data frame libraries
import numpy as np
import pandas as pd
import geopandas as gpd

import os

# plotting libraries
from mpl_toolkits.basemap import Basemap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.collections import PatchCollection

from shapely.ops import transform
from shapely.geometry import Point, Polygon
from descartes import PolygonPatch

# suppress matplotlib/basemap warnings
import warnings
warnings.filterwarnings("ignore")

# local NAME libraries
from grid import gridsquare
from header import loadheader

# ------------------------------------
# input shapefile name/colour list

shapelist = "europe_shapes.list"
files = []
colors = []

with open(shapelist, 'r') as f:

    for line in f:
        if "," in line:
            (filename, colorname) = line.split(",",1)
            filename = filename.strip()
            colorname = colorname.strip()

            files.append(filename)
            colors.append(colorname)

#print files
#print colors

# ------------------------------------
# input NAME filename
filename = 'PML_NAME_output/low5dayPML_20150501.txt'

# Map bounds

lon_bounds = [-20., 20. ]
lat_bounds = [ 40., 60. ]

lon_axis = [ -20., -10., 0., 10 ]
lat_axis = [ 45., 50., 55., 60. ]

lon_pml = -4.1931
lat_pml = 50.3189

# ------------------------------------
print 'Loading ' + filename + '...',

# read and parse NAME file header
header = loadheader(filename)

# get grid size from header
delta_lon = float(header['X grid resolution'])
delta_lat = float(header['Y grid resolution'])
grid_size = (delta_lon, delta_lat)

# read CSV portion of NAME file into pandas DataFrame
df = pd.read_csv(filename, header=31)

# Clear bad (empty) data columns from DataFrame
df = df.dropna(axis=1, how='all')

# Get column header timestamp names from first row
c = map(list, df[0:1].values)
collist = c[0]

# Set leader column names
collist[1:4] = ['X-Index', 'Y-Index', 'Longitude', 'Latitude']
collist = [ x.strip() for x in collist ]

# Get observation timestamp strings
timestamps = collist[5::]

# Apply labels to DataFrame
df.columns = collist[1::]

# Drop leading rows
df = df.drop([0,1,2,3])

# Convert strings to floats where possible
df = df.apply(lambda x: pd.to_numeric(x, errors='ignore'))

# Set mapping coordinate for GeoDataFrame
crs = {'init': 'epsg:4326'}

# Generate Shapely Point objects for each grid point
df['points'] = [ Point(xy) for xy in zip(df.Longitude, df.Latitude) ]

# Generate Shapely Polygons for grid squares
df['grid'] = [ Polygon(gridsquare(xy + grid_size)) for xy in zip(df.Longitude, df.Latitude) ]

# Create GeoDataFrame with point and grid geometry columns
geo_df = gpd.GeoDataFrame(df, crs=crs, geometry=df['points'])

print 'done'

# Get minimum non-zero concentration value
cl = geo_df[timestamps].values.tolist()
flat = [ item for sublist in cl for item in sublist ]
min_conc = min([ x for x in flat if x > 0.0 ])

# Get maximum concentration value
max_conc = geo_df[timestamps].values.max()

print "Min concentration: ", min_conc
print "Max concentration: ", max_conc

# ------------------------------------
# begin plotting

print 'Plotting figure...',

# set timestamp
ts = '26/04/2015 00:00 UTC'

# initialise plot
fig, ax = plt.subplots()

ax.set_aspect('equal')

# set normalisation
norm = matplotlib.colors.LogNorm(vmin=min_conc, vmax=max_conc, clip=False)

m = Basemap(llcrnrlon=lon_bounds[0], llcrnrlat=lat_bounds[0],
                                    urcrnrlon=lon_bounds[1], urcrnrlat=lat_bounds[1],
                                    projection='cyl', lat_1=45., lat_2=55., lon_0=0.,
                                    resolution='l', area_thresh=1000.)

m.drawcoastlines(color='white')
m.drawcountries(color='white')
m.drawmapboundary(fill_color='#444444')
m.fillcontinents(color='#bbbbbb',lake_color='#444444')
m.drawparallels(lat_axis, linewidth=0.5, color='white', labels=[1,0,0,1])
m.drawmeridians(lon_axis, linewidth=0.5, color='white', labels=[1,0,0,1])

ax.set_title('filename, fontsize=12')


# Loop over input shapefiles

patches = []

for shapefile in files:

    # read ESRI shapefile into GeoPandas object
    shape = gpd.GeoDataFrame.from_file(shapefile)
    
    for poly in shape.geometry:
        if poly.geom_type == 'Polygon':
#            print 'polygon found', poly
            mpoly = transform(m, poly)
            patches.append(PolygonPatch(mpoly))
        elif poly.geom_type == 'MultiPolygon':
            for subpoly in poly:
#                print 'subpolygon found', subpoly
                mpoly = transform(m, subpoly)
                patches.append(PolygonPatch(mpoly))
    else:
        pass
#        print 'Neither a polygon for a multi-polygon'

pc  = PatchCollection(patches, match_original=True)
pc.set_facecolor(colors)
pc.set_edgecolor('none')
pc.set_alpha(0.5)
pc.set_zorder(4)

sq = ax.add_collection(pc)

# ------------------------------------

gpatches = []

for poly in geo_df['grid']:
    mpoly = transform(m, poly)
    gpatches.append(PolygonPatch(mpoly))

gpc = PatchCollection(gpatches, cmap=cm.rainbow, norm=norm, match_original=True)
gpc.set_edgecolor('none')
gpc.set_zorder(10)
gpc.set(array=geo_df[ts])

gsq = ax.add_collection(gpc)

fig.text(0.4, 0.15, ts, color='white', transform=ax.transAxes)

fig.colorbar(gpc, label=r'Concentration (g s/m$^3$)', shrink=0.7)

# ------------------------------------

# plot PML site marker
x_pml, y_pml = m(lon_pml, lat_pml)
m.plot(x_pml, y_pml, 'kx', markersize=12, zorder=10)

# ------------------------------------

pngfile = 'plot_europe_grid.png'
fig.savefig(pngfile, dpi=300)

print 'done.'
