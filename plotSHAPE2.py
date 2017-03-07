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
# input shapefile name
shapefile = "PML_shapefiles/UK_coast"
shape = 'UK_coast'

# Map bounds

lon_bounds = [-20., 20. ]
lat_bounds = [ 40., 60. ]

lon_axis = [ -20., -10., 0., 10 ]
lat_axis = [ 45., 50., 55., 60. ]

# ------------------------------------
# initialise plot
fig = plt.figure()
ax = fig.add_subplot(111)

ax.set_aspect('equal')

m = Basemap(llcrnrlon=lon_bounds[0], llcrnrlat=lat_bounds[0],
                                    urcrnrlon=lon_bounds[1], urcrnrlat=lat_bounds[1],
                                    projection='lcc', lat_1=45., lat_2=55., lon_0=0.,
                                    resolution='l', area_thresh=1000.)

m.drawcoastlines(color='white')
m.drawcountries(color='white')
m.drawmapboundary(fill_color='#444444')
m.fillcontinents(color='#bbbbbb',lake_color='#444444')
m.drawparallels(lat_axis, linewidth=0.5, color='white')
m.drawmeridians(lon_axis, linewidth=0.5, color='white')

ax.set_title('Testing ESRI plot...')

s = m.readshapefile(shapefile, shape)


patches = []

for s in m.UK_coast:
    patches.append( Polygon(np.array(s), True) )

pc  = PatchCollection(patches, facecolor='green', edgecolor='blue', match_original=True)
pc.set_edgecolor('blue')
pc.set_zorder(4)

sq = ax.add_collection(pc)

pngfile = 'plot_europe1a.png'
fig.savefig(pngfile, dpi=300)

print 'done.'
