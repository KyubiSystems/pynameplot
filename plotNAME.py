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
from geopandas import GeoDataFrame

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

# ---------------------------------------
# input filename
filename = '1daysurfaceWARRI_20110715.txt'

# Map bounds
lon_bounds = [ 2., 7. ]
lat_bounds = [ 1., 8. ]

lon_axis = [4., 6.]
lat_axis = [2., 4., 6.]

lon_warri = 5.5
lat_warri = 6.0

# ---------------------------------------
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
geo_df = GeoDataFrame(df, crs=crs, geometry=df['points'])

print 'done'

#print geo_df[timestamps]
#print geo_df['14/07/2011 15:00 UTC']

#print df['Longitude'].max()
#print df['Longitude'].min()

#print df['Latitude'].max()
#print df['Latitude'].min()

# Get minimum non-zero concentration value
cl = geo_df[timestamps].values.tolist()
flat = [ item for sublist in cl for item in sublist ]
min_conc = min([ x for x in flat if x > 0.0 ])

# Get maximum concentration value
max_conc = geo_df[timestamps].values.max()

print "Min concentration: ", min_conc
print "Max concentration: ", max_conc

# ---------------------------------------
# begin plotting

print "Plotting figure...",

# set timestamp
ts = '14/07/2011 15:00 UTC'

fig = plt.figure()
ax = fig.add_subplot(111)

ax.set_aspect('equal')

# set normalisation
norm = matplotlib.colors.LogNorm(vmin=min_conc, vmax=max_conc, clip=False)

m = Basemap(llcrnrlon=lon_bounds[0], llcrnrlat=lat_bounds[0],
                        urcrnrlon=lon_bounds[1], urcrnrlat=lat_bounds[1],
                        projection='lcc', lat_1=2., lat_2=6., lon_0=4.,
                        resolution='i', area_thresh=1000.)

m.drawcoastlines(color='white', zorder=8)
m.drawcountries(color='white', zorder=8)
m.drawmapboundary(fill_color='#444444')
m.fillcontinents(color='#bbbbbb',lake_color='#444444')
m.drawparallels(lat_axis, linewidth=0.5, color='white', labels=[1,0,0,1], zorder=8)
m.drawmeridians(lon_axis, linewidth=0.5, color='white', labels=[1,0,0,1], zorder=8)

ax.set_title(filename, fontsize=12)

patches = []

for poly in geo_df['grid']:
    mpoly = transform(m, poly)
    patches.append(PolygonPatch(mpoly))


pc = PatchCollection(patches, cmap=cm.rainbow, norm=norm, match_original=True)
pc.set_edgecolor('none')
pc.set_zorder(4)
pc.set(array=geo_df[ts])

sq = ax.add_collection(pc)

fig.text(0.4, 0.15, ts, color='white', transform=ax.transAxes)

fig.colorbar(pc, label=r'Concentration (g s/m$^3$)', shrink=0.7)

# plot WARRI
x_warri, y_warri = m(lon_warri, lat_warri)
m.plot(x_warri, y_warri, 'kx', markersize=12, zorder=10)

pngfile = 'plot_test4c.png'
fig.savefig(pngfile, dpi=300)

print "done"




