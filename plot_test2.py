#!/usr/bin/env python

from mpl_toolkits.basemap import Basemap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from shapely.ops import transform
from shapely.geometry import Polygon
from descartes import PolygonPatch

import warnings
warnings.filterwarnings("ignore")

title = '1daysurfaceWARRI_20110715.txt'

lon_bounds = [ 2., 7. ]
lat_bounds = [ 1., 8. ]

lon_axis = [4., 6.]
lat_axis = [2., 4., 6.]

lon = 2.5
lat = 2.5

fig = plt.figure()
ax = fig.add_subplot(111)

ax.set_aspect('equal')

m = Basemap(llcrnrlon=lon_bounds[0], llcrnrlat=lat_bounds[0],
            urcrnrlon=lon_bounds[1], urcrnrlat=lat_bounds[1],
            projection='lcc', lat_1=2., lat_2=6., lon_0=4.,
            resolution='i', area_thresh=1000.)

m.drawcoastlines(color='white')
m.drawcountries(color='white')
m.drawmapboundary(fill_color='#444444')
m.fillcontinents(color='#bbbbbb',lake_color='#444444')
m.drawparallels(lat_axis, linewidth=0.5, color='white')
m.drawmeridians(lon_axis, linewidth=0.5, color='white')

ax.set_title(title, fontsize=12)

patches = []
poly = Polygon([(lon, lat), (lon-0.25, lat), (lon-0.25, lat-0.25), (lon, lat-0.25)])
mpoly = transform(m, poly)
patches.append(PolygonPatch(mpoly))

sq = ax.add_collection(PatchCollection(patches, match_original=True))

pngfile = 'plot_test2.png'
fig.savefig(pngfile, dpi=300)
