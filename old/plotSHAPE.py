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

import os
import geopandas as gpd

# plotting libraries
from mpl_toolkits.basemap import Basemap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection

from shapely.ops import transform
from shapely.geometry import Point, Polygon
from descartes import PolygonPatch

# suppress matplotlib/basemap warnings
import warnings
warnings.filterwarnings("ignore")

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
# Map bounds

lon_bounds = [-20., 20. ]
lat_bounds = [ 40., 60. ]

lon_axis = [ -20., -10., 0., 10 ]
lat_axis = [ 45., 50., 55., 60. ]

# ------------------------------------
# initialise plot
fig, ax = plt.subplots()

ax.set_aspect('equal')

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

ax.set_title('Testing ESRI plot...')


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
        print 'Neither a polygon for a multi-polygon'

pc  = PatchCollection(patches, match_original=True)
pc.set_facecolor(colors)
pc.set_edgecolor('none')
pc.set_alpha(0.5)
pc.set_zorder(4)

sq = ax.add_collection(pc)

pngfile = 'plot_europe2.png'
fig.savefig(pngfile, dpi=300)

print 'done.'
