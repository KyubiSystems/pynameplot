#!/usr/bin/env python

from mpl_toolkits.basemap import Basemap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

lon_bounds = [ 2., 7. ]
lat_bounds = [ 1., 8. ]

fig, ax = plt.subplots()

ax.set_aspect('equal')

m = Basemap(llcrnrlon=lon_bounds[0], llcrnrlat=lat_bounds[0],
            urcrnrlon=lon_bounds[1], urcrnrlat=lat_bounds[1],
            projection='lcc', lat_1=2., lat_2=6., lon_0=4.,
            resolution='l', area_thresh=1000.)

m.shadedrelief()

ax.set_title('Test Basemap plot', fontsize=20)

pngfile = 'plot_test_shaded.png'
fig.savefig(pngfile, dpi=300)
