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

from configobj import ConfigObj

# local NAME libraries
from namereader import *

# ------------------------------------

parser = argparse.ArgumentParser(prog='plotter', description='Plot NAME concentration files on world map')
parser.add_argument("-c", "--config", help="Configuration file", required=True)

args = parser.parse_args()

# ------------------------------------
# Configuration options

config = ConfigObj(args.config)

shapelist = config['shapelist']  # Text file containing list of shapefiles
infile = config['infile']  # Single input NAME file
indir = config['indir']  # Directory containing input NAME files

infile2 = config['infile2']   # Optional second input NAME file
indir2 = config['indir2']    # Optional second directory containing input NAME files

timestamp = config['timestamp']  # Plot data for given timestamp
day = config['day']   # Plot data summed for given day
week = config['week']   # Plot data summed for given week
month = config['month']   # Plot data summed for given month
year = config['year']    # Plot data summed for given year

projection = config['projection']  # Map projection 

lon_bounds = config['lon_bounds']  # (Long_min, Long_max) tuple: Longitude bounds of plot
lat_bounds = config['lat_bounds']  # (Lat_min, Lat_max) tuple: Latitude bounds of plot

lon_axis = config['lon_axis']  # (Lon1, Lon2, Lon3...) tuple: Lon scale tickmarks
lat_axis = config['lat_axis']  # (Lat1, Lat2, Lat3...) tuple: Lat scale tickmarks

scale = config['scale'] # (Min, Max) scale tuple for plotting values, default is autoscale

colormap = config['colormap']  # Colourmap name

solid = config['solid']  # Set solid flag
color1 = config['color1']   # Solid colour for dataset 1
color2 = config['color2']   # Solid colour for dataset 2

station = config['station']  # (Lon, Lat) tuple containing Station coordinates

outfile = config['outfile']  # Output plot file name root

# ------------------------------------

# read NAME data into object
n = namereader.Name(infile)

# Create Map object from NAME data
m = namereader.Map(name)

if not scale:
    m.autoScale()
else:
    (scale_min, scale_max) = scale
    m.setScale(scale_min, scale_max)
