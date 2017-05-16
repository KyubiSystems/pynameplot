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

import argparse
import numpy as np
import pandas as pd
import geopandas as gpd
import itertools

from shapely import speedups
from shapely.geometry import Polygon

from namereader import *

if speedups.available:
    speedups.enable()

# ------------------------------------

parser = argparse.ArgumentParser(prog='makemastergrid', description='Generate master grid file from ESRI zones.')
parser.add_argument("-n", "--namefile", help='Input NAME file to define grid shape', required=True)
parser.add_argument("-s", "--shapelist", help='File containing list of input shapefiles', required=True)
parser.add_argument("-o", "--outfile", help='Output master grid file name', required=True)
args = parser.parse_args()

print '+++ Starting makemastergrid... +++'

#namefile = 'PML_NAME_output/low5dayPML_20150501.txt'  # input NAME filename
#shapelist = "europe_shapes.list"  # shapefile name/colour list
#outfile = "PML.pickle2"  # output pickle

# ------------------------------------
# Read list of shapefiles, colours

print "Reading shape list %s..." % args.shapelist

files = []
colors = []

with open(args.shapelist, 'r') as shp:

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
# Read NAME file header for grid parameters

print "Parsing header %s..." % args.namefile

head = header.loadheader(args.namefile)

x0 = float(head['X grid origin'])
y0 = float(head['Y grid origin'])
xsize = float(head['X grid size'])
ysize = float(head['Y grid size'])
xstep = float(head['X grid resolution'])
ystep = float(head['Y grid resolution'])

grid_size = (xstep, ystep)

x1 = x0 + ((xsize-1) * xstep)
y1 = y0 + ((ysize-1) * ystep)

xcol = np.linspace(x0, x1, xsize)  # Longitude axis
ycol = np.linspace(y0, y1, ysize)  # Latitude axis

longitude = []
latitude = []

for (colx, coly) in itertools.product(xcol, ycol):
    longitude.append(colx)
    latitude.append(coly)

# ------------------------------------

data = { 'Longitude': longitude, 'Latitude': latitude }
df = pd.DataFrame(data)
df = df[['Longitude', 'Latitude']]  # Set column order manually

# Generate grid lat-long index for subsequent matching
# print 'Generating Lat-Long index...',
# df.set_index(['Longitude', 'Latitude'], drop=False, inplace=True)
# print 'done.'

# Generate polygon geometry column
df['grid'] = [ Polygon(geom.gridsquare(xy + grid_size)) for xy in zip(df.Longitude, df.Latitude) ]

# Set mapping coordinate for GeoDataFrame
crs = {'init': u'epsg:4326'}

# Create GeoDataFrame
gd = gpd.GeoDataFrame(df, crs=crs, geometry=df['grid'])

print "Starting covering factor calculations..."

# Loop over input shapefiles
for f in files:

    shp = shape.Shape(f)
    print "Processing zone %s..." % shp.shortname

    cover = gpd.sjoin(gd, shp.data, how='inner', op='intersects')

    cover[shp.shortname] = [geom.coverfactor(shp.proj_cu, s, shp.lat_min, shp.lat_max) for s in cover['grid']]

    c2 = cover[shp.shortname]

    if not c2.index.is_unique:

        print "Removing duplicate index for %s" % shp.shortname
        c2 = c2[~c2.index.duplicated(keep='first')]


    gd = gd.join(c2)

# Replacing NaNs
gd = gd.fillna(0)

gd = gd.set_index(['Longitude', 'Latitude'])

# Set sparse to reduce on-disk filesize
gd = gd.to_sparse(fill_value=0)

# Write pickle file
print "Writing output file %s..." % args.outfile
gd.to_pickle(args.outfile)

print "=== Done! ==="
