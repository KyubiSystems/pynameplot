#!/usr/bin/env python

from mpl_toolkits.basemap import Basemap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

title = '1daysurfaceWARRI_20110715.txt'

lon_bounds = [ 2., 7. ]
lat_bounds = [ 1., 8. ]

lon_axis = [4., 6.]
lat_axis = [2., 4., 6.]

fig, ax = plt.subplots()

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

pngfile = 'plot_test.png'
fig.savefig(pngfile, dpi=300)
