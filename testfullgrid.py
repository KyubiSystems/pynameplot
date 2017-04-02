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

import numpy as np
import pandas as pd
import itertools

from shapely import speedups
from shapely.geometry import Polygon

from namereader import *

# input NAME filename
filename = 'PML_NAME_output/low5dayPML_20150501.txt'

# shapefile name/colour list
shapelist = "europe_shapes.list"

# output pickle
outfile = "PML.pickle"


if speedups.available:
    speedups.enable()


# ------------------------------------

files = []
colors = []

with open(shapelist, 'r') as shp:

    for line in shp:
        if "," in line:
            (shapename, colorname) = line.split(",", 1)
            shapename = shapename.strip()
            colorname = colorname.strip()

            files.append(shapename)
            colors.append(colorname)

shortnames = [ util.shortname(f) for f in files ]
pcnames = [ 'pc_' + s for s in shortnames ]

# ------------------------------------

head = header.loadheader(filename)

x0 = float(head['X grid origin'])
y0 = float(head['Y grid origin'])
xsize = float(head['X grid size'])
ysize = float(head['Y grid size'])
xstep = float(head['X grid resolution'])
ystep = float(head['Y grid resolution'])

grid_size = (xstep, ystep)

x1 = x0 + ((xsize-1) * xstep)
y1 = y0 + ((ysize-1) * ystep)

xcol = np.linspace(x0, x1, xsize)
ycol = np.linspace(y0, y1, ysize)

longitude = []
latitude = []

for (colx, coly) in itertools.product(xcol, ycol):
    longitude.append(colx)
    latitude.append(coly)

data = { 'Longitude': longitude, 'Latitude': latitude }

df = pd.DataFrame(data)

df['grid'] = [ Polygon(geom.gridsquare(xy + grid_size)) for xy in zip(df.Longitude, df.Latitude) ]

print "Starting covering factor calculations..."

# Loop over input shapefiles
for f in files:

    shp = shape.Shape(f)

    print "Processing %s..." % shp.shortname

    # calculate covering factor column
    df[shp.shortname] = [geom.coverfactor(shp.proj_geo, s, shp.lat_min, shp.lat_max) for s in df['grid']]

print "Done!"

df = df.to_sparse(fill_value=0)

df.to_pickle(outfile)
