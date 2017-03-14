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

from shapely import speedups
from shapely.ops import transform
from shapely.geometry import Point, Polygon

import pyproj

import os

from functools import partial

# local NAME libraries
from grid import gridsquare
from header import loadheader
from geom import reproj, coverfactor, shortname

# --------------------------------------
# Enable C++ native acceleration for Shapely processing
if speedups.available:
    speedups.enable()
# --------------------------------------
# input shapefile name/colour list

shapelist = 'europe_shapes.list'
files = []
colors = []

# test input grid square
square = Polygon([(10,50),(10,51),(9,51),(9,50)])

with open(shapelist, 'r') as f:
    
    for line in f:
        if "," in line:
            (filename, colorname) = line.split(",", 1)
            filename = filename.strip()
            colorname = colorname.strip()

            files.append(filename)
            colors.append(colorname)

for shapefile in files:

    print shortname(shapefile)
    
    # read ESRI shapefile into GeoPandas object
    shape = gpd.GeoDataFrame.from_file(shapefile)

    # get Shapely geometry from GeoPandas object
    geo = shape.geometry

    # Detemine geometric covering factor
    cf = coverfactor(geo, square)

    print 'Covering factor: ', cf

    
