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
import os

from configobj import ConfigObj

# local NAME libraries
from namereader import *

"""
- plotter.py -

Read named configuration file
Load input NAME file, or subset of NAME files in directory
Set plot extent, normalisatiom, colormap, caption
Plot data mesh on Basemap
Save output to disk
"""

parser = argparse.ArgumentParser(prog='plotter', description='Plot NAME concentration files on world map')
parser.add_argument("-c", "--config", help="Configuration file", required=True)

args = parser.parse_args()

# ------------------------------------
# Configuration options

if not os.path.isfile(args.config):
    exit('*** ERROR: Configuration file {} not found!'.format(args.config))

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
projection = config.get('projection')  # Map projection, default is 'cyl' (Cylindrical)
lon_bounds = config.get('lon_bounds')  # (Long_min, Long_max) tuple: Longitude bounds of plot
lat_bounds = config.get('lat_bounds')  # (Lat_min, Lat_max) tuple: Latitude bounds of plot
lon_axis = config.get('lon_axis')  # (Lon1, Lon2, Lon3...) tuple: Lon scale tickmarks
lat_axis = config.get('lat_axis')  # (Lat1, Lat2, Lat3...) tuple: Lat scale tickmarks

# map colour
scale = config.get('scale') # (Min, Max) scale tuple for plotting values, default is (5e-9, 1e-4)
autoscale = config.get('autoscale') # Set flag for scaling colormap by min/max data values

colormap = config.get('colormap')  # Matplotlib colormap name to be used for data, default is 'rainbow'

solid = config.get('solid')  # Set flag for solid region plotting
color1 = config.get('color1')   # Solid colour for dataset 1
color2 = config.get('color2')   # Solid colour for dataset 2

# map labelling
caption = config.get('caption')  # Primary caption for output plot

# output directory
outdir = config.get('outdir')  # Output directory for plot files, create if does not exist

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
        exit();
    elif week:
        s.sumWeek(week)
        if not caption:
            caption = "{} {} {} {}: summed week {}". format(s.runname, s.averaging, s.altitude, s.direction, week)
        if not outfile:
            outfile = "{}_sum_week_{}.png".format(s.runnname, week)

    elif month:
        s.sumMonth(month)
        if not caption:
            caption = "{} {} {} {}: summed month {}". format(s.runname, s.averaging, s.altitude, s.direction, month)
        if not outfile:
            outfile = "{}_sum_month_{}.png".format(s.runname, month)

    elif year:
        s.sumYear(year)
        if not caption:
            caption = "{} {} {} {}: summed year {}". format(s.runname, s.averaging, s.altitude, s.direction, year)
        if not outfile:
            outfile = "{}_sum_year_{}.png".format(s.runname, year)

    else:
        raise ValueError('Unrecognised or undefined timespan')
        exit()
    
    n = s

else:
    raise ValueError('No input file or directory defined')
    exit

# Create Map object from NAME data
m = namemap.Map(n, column=column)

# Set projection if defined, otherwise cylindrical
if projection:
    m.setProjection(projection)

# Set map bounds from config file, otherwise scale by grid file
if lon_bounds and lat_bounds:
    m.setBounds(lon_bounds, lat_bounds)
else:
    m.setBounds(n.lon_bounds, n.lat_bounds)

# Set map axes from config file, else scale by grid file
if lon_axis and lat_axis:
    lon = [float(i) for i in lon_axis]
    lat = [float(i) for i in lat_axis]
    m.setAxes(lon, lat)
else:
    m.setAxes(n.lon_grid, n.lat_grid)

# Set scale if defined, otherwise standard scale
# set other option for autoscale?
if scale:
    (scale_min, scale_max) = scale
    m.setFixedScale(scale_min, scale_max)
elif autoscale:
    m.setAutoScale(column)

# Set up data grid
if caption:
    m.drawBase(caption)
else:
    m.drawBase(n.caption, fontsize=8)


# Check for solid colouring flag
if solid:
    m.solid = True
    if color1:
        m.drawSolid(column, color=color1)
    else:
        m.drawSolid(column)

# Plot using colormap
elif colormap:
    m.setColormap(colormap)
    m.drawMesh(column)
else:
    m.setColormap()
    m.drawMesh(column)

# m.addTimestamp()

# Add station markers 1-6 if defined
station_list = ['station1', 'station2', 'station3', 'station4', 'station5', 'station6']
for station_name in station_list:
    station = config.get(station_name)
    if station:
        (station_lon, station_lat) = station
        m.addMarker(station_lon, station_lat)

# If output directory does not exist, create it
if outdir:
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    m.outdir = outdir

# Save output to disk
if outfile:
    m.saveFile(filename=outfile)
else:
    m.saveFile()
