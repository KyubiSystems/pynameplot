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

"""
- plotter.py -

Read named configuration file
Load input NAME file, or subset of NAME files in directory
Set plot parameters
Load NAME data into grid geometry
Plot grid on Basemap
Save output to disk
"""

parser = argparse.ArgumentParser(prog='plotter', description='Plot NAME concentration files on world map')
parser.add_argument("-c", "--config", help="Configuration file", required=True)

args = parser.parse_args()

# ------------------------------------
# Configuration options

config = ConfigObj(args.config, raise_errors=True, list_values=True)

# Reading configuration values

# input path
shapelist = config.get('shapelist') # Text file containing list of shapefiles
infile = config.get('infile') # Single input NAME file
indir = config.get('indir')  # Directory containing input NAME files

# secondary input path
infile2 = config.get('infile2')   # Optional second input NAME file
indir2 = config.get('indir2')    # Optional second directory containing input NAME files

# time select
timestamp = config.get('timestamp')  # Plot data for given timestamp
day = config.get('day')   # Plot data summed for given day
week = config.get('week')   # Plot data summed for given week
month = config.get('month')   # Plot data summed for given month
year = config.get('year')    # Plot data summed for given year

# map geometry
projection = config.get('projection')  # Map projection 
lon_bounds = config.get('lon_bounds')  # (Long_min, Long_max) tuple: Longitude bounds of plot
lat_bounds = config.get('lat_bounds')  # (Lat_min, Lat_max) tuple: Latitude bounds of plot
lon_axis = config.get('lon_axis')  # (Lon1, Lon2, Lon3...) tuple: Lon scale tickmarks
lat_axis = config.get('lat_axis')  # (Lat1, Lat2, Lat3...) tuple: Lat scale tickmarks

# map colour
scale = config.get('scale') # (Min, Max) scale tuple for plotting values, default is autoscale

colormap = config.get('colormap')  # Colourmap name

solid = config.get('solid')  # Set solid flag
color1 = config.get('color1')   # Solid colour for dataset 1
color2 = config.get('color2')   # Solid colour for dataset 2

# map labelling
station = config.get('station')  # (Lon, Lat) tuple containing Station coordinates
caption = config.get('caption')  # Primary caption for output plot

# output file
outfile = config.get('outfile')  # Output plot file name root

# ------------------------------------


# read NAME data into object

if infile:
    n = name.Name(infile)
    if timestamp:
        column = timestamp
    else:
        n.sum_all()
        column = 'total'


elif indir:
    s = namesum.Sum(indir)
    column = 'total'

    if day:
        print 'not yet implemented'
        exit;
    elif week:
        n = s.weeks[week]
    elif month:
        n = s.months[month]
    elif year:
        n = s.years[year]
    else:
        raise ValueError('Unrecognised or undefined timespan')
        exit

else:
    raise ValueError('No input file or directory defined')
    exit

# Create Map object from NAME data
m = namemap.Map(n, column=column)

# Set projection if defined, otherwise cylindrical
if projection:
    m.setProjection(projection)

# Set map bounds 
if lon_bounds and lat_bounds:
    m.setBounds(lon_bounds, lat_bounds)
else:
    raise ValueError('Unrecognised or undefined map bounds lon_range, lat_range')
    exit

# Set map axis 
if lon_axis and lat_axis:
    lon = [float(i) for i in lon_axis]
    lat = [float(i) for i in lat_axis]
    m.setAxes(lon, lat)
else:
    raise ValueError('Unrecognised or undefined map axes lon_axis, lat_axis')
    exit

# Set scale if defined, otherwise autoscale
if scale:
    (scale_min, scale_max) = scale
    m.setScale(scale_min, scale_max)

# Set up data grid
m.drawBase()
m.gridSetup()

# Check for solid colouring flag
if solid:
    if color1:
        m.gridSolid(color=color1)
    else:
        m.gridSolid()

# Set colourmap
if colormap:
    m.gridColormap(colormap)
else:
    m.gridColormap()

# Draw gridded values
m.gridDraw()
m.addTimestamp()

# Add station marker if defined
if station:
    (station_lon, station_lat) = station
    m.addMarker(station_lon, station_lat)

# Save output to disk
if outfile:
    m.saveFile(filename=outfile)
else:
    m.saveFile()
