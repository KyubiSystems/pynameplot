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

# input NAME filename
namefile = '../data/PML_NAME_output/low5dayPML_20150501.txt'

# input shapefile name/colour list
shapelist = "europe_shapes.list"

# output CSV filename
outfile = "testdata.csv"

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

# Instantiate NAME object
name = name.Name(namefile)
timestamps = name.timestamps  

print "Starting covering factor calculations..."

for f in files:
    print "Processing %s..." % util.shortname(f)
    name.get_cover(f)

print "Done"

print "Writing to %s" % outfile

with open(outfile, 'w') as csvfile:

    fieldnames = ["Timestamp"] + shortnames + pcnames
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
    writer.writeheader()
    
    for t in timestamps:
        print t

        totals = {}
        percents = {}
        
        for s in shortnames:
            totals[s] = (name.data[t] * name.data[s]).sum()

        sum_conc = sum(totals.values())
        for s in shortnames:
            percents[ 'pc_' + s ] = (totals[s] / sum_conc) * 100.0
        
        row = util.merge_dicts({ "Timestamp" : t }, totals, percents)
        writer.writerow(row)

