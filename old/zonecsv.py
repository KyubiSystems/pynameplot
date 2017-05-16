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

parser = argparse.ArgumentParser(prog='zonecsv', description="Sum NAME concentration files over ESRI zones.")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-d", "--indir", help="Input NAME file directory")
group.add_argument("-n", "--namefile", help="Input NAME file to sum over")
parser.add_argument("-g", "--grid", help="Input master grid file", required=True)
parser.add_argument("-o", "--outfile", help="Output CSV results file", required=True)
group2 = parser.add_mutually_exclusive_group()
group2.add_argument("-w", "--week", help="Select NAME files from ISO week number")
group2.add_argument("-m", "--month", help="Select NAME files from Month number")
group2.add_argument("-y", "--year", help="Select NAME files from Year")

args = parser.parse_args()

# namefile = 'PML_NAME_output/low5dayPML_20150501.txt'  # input NAME filename 
# pklfile = 'PML_master.pkl'  # input master grid file
# outfile = "testdata2.csv"  # output csv filename

# -------------------------------------

# Load zone gridfile
zones = pd.read_pickle(args.grid)
zones = zones.to_dense()
zones = zones.fillna(0)
print "Loaded master grid file %s..." % args.grid

# 
if args.namefile:
    files = [args.namefile]

if args.indir:
    f = fileset.Fileset(args.indir)
    if args.week:
        files = f.weeks[args.week]
    elif args.month:
        files = f.months[args.month]
    elif args.year:
        files = f.years[args.year]
    else:
        files = f.getAll()

print "Writing output file %s..." % args.outfile

with open(args.outfile, 'w') as csvfile:

    # Generate zone column names
    shortnames = list(zones)[2::]
    pc_cols = ['pc_' + s for s in shortnames]
    fieldnames = ['Timestamp'] + shortnames + pc_cols

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
    writer.writeheader()

    for n in sorted(files):

        # Instantiate NAME object from file
        namefile = name.Name(n)
        timestamps = namefile.timestamps
        namedata = namefile.data
        print "Loaded NAME file %s..." % n

        for t in timestamps:
            print "Processing time %s..." % t

            totals = {}
            percents = {}
            sum_conc = 0.0

            d = namedata[t]

            for s in shortnames:

                z = zones[s]
                totals[s] = (d * z).sum()   # lat/lon indexed multiplication 
                
            sum_conc = sum(totals.values())
        
            for s in shortnames:
                percents['pc_' + s] = (totals[s] / sum_conc) * 100.0   # Calculate zone percentages

            row = util.merge_dicts({"Timestamp": t}, totals, percents)

            writer.writerow(row)

print "Done!"
