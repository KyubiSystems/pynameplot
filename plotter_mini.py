#!/usr/bin/env python

from namereader import *
import matplotlib
import matplotlib.cm as cm
import pandas as pd

infile = 'PML_NAME_output/low5dayPML_20150501.txt'
timestamp = '26/04/2015 00:00 UTC'

n = name.Name(infile)
column = timestamp

mm = namemap.Map(n, column=column)

mm.setBounds(n.lon_bounds, n.lat_bounds)

mm.setAxes(n.lon_grid, n.lat_grid)

mm.setScale((5.0e-9, 1.0e-4))

mm.drawBase('test of colormesh')

foo = n.data[timestamp]

foo1 = foo.loc[foo > 0.0]

foo2 = foo1.unstack(level=1)
foo2 = foo2.fillna(0)

lons = foo2.index.get_level_values('Longitude')
lats = foo2.columns

foo2 = foo2.transpose()

x,y = mm.m(lons,lats)

norm = matplotlib.colors.LogNorm(vmin=5e-9, vmax=1e-4, clip=False)

mm.m.pcolormesh(x, y, foo2, cmap=cm.rainbow, norm=norm, zorder=4)

mm.saveFile(filename='plot_minitest.png')

