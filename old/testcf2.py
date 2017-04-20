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

import csv
from namereader import *

# instantiate new NAME object
name = name.Name('PML_NAME_output/low5dayPML_20150501.txt')

# ------------------------------------
# input shapefile name/colour list

outfile = 'PML_testout.csv'

shapelist = "europe_shapes.list"
files = []
colors = []

with open(shapelist, 'r') as f:

    for line in f:
        if "," in line:
            (filename, colorname) = line.split(",",1)
            filename = filename.strip()
            colorname = colorname.strip()

            files.append(filename)
            colors.append(colorname)

# ------------------------------------
# Generate covering factor column for input ESRI shapefile                                                                                                                           
print 'Starting covering factor calculation...',

for shape in files:
    print 'Reading %s...' % util.shortname(shape)
    name.get_cover(shape)

short = [util.shortname(f) for f in files]

with open(outfile, 'a') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
    title = ['Timestamp'] + short
    writer.writerow(title)

    for t in name.timestamps:
        row = [t]
        for s in short:  # iterate over zones
            zonesum = (name.data[t] * name.data[s]).sum() # calculate total zone concentration
            row.append(zonesum)

        writer.writerow(row)
            
