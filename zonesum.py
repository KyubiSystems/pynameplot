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
import pandas as pd
import csv
from namereader import *

# -------------------------------------

parser = argparse.ArgumentParser(prog='zonesum', description="Sum NAME concentration files over ESRI zones.")
parser.add_argument("-n", "--namefile", help="Input NAME file to sum over", required=True)
parser.add_argument("-m", "--grid", help="Input master grid file", required=True)
parser.add_argument("-o", "--outfile", help="Output CSV results file", required=True)
args = parser.parse_args()

# namefile = 'PML_NAME_output/low5dayPML_20150501.txt'  # input NAME filename 
# pklfile = 'PML_master.pkl'  # input master grid file
# outfile = "testdata2.csv"  # output csv filename

# -------------------------------------

# Load zone gridfile
zones = pd.read_pickle(args.grid)
zones = zones.to_dense()
print "Loaded master grid file %s..." % pklfile

# WILL LOOP OVER NAME FILES HERE ====
# Instantiate NAME object from file
name = name.Name(args.namefile)
timestamps = name.timestamps
data = name.data
print "Loaded NAME file %s..." % namefile

# Generate zone column names
columns = list(zones)[3::]
pc_cols = [ 'pc_' + c for c in columns ]
fieldnames = ['Timestamp'] + columns + pc_cols

# -------------------------------------

with open(args.outfile, 'w') as csvfile:

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
    writer.writeheader()

    for t in timestamps:
        print "Processing time %s..." % t

        print data[t]

        totals = {}
        precents = {}

        for s in shortnames:
            totals[s] = (data[t] * zone[s]).sum()   # Try lat/lon indexed multiplication here

        sum_conc = sum(totals.values())

        for s in shortnames:
            percents[ 'pc_' + s ] = (totals[s] / sum_conc) * 100.0

        row = util.merge_dicts({ "Timestamp" : t }, totals, percents)
        writer.writerow(row)


