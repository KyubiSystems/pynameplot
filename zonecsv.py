#!/usr/bin/env python

# Author: Duncan Law-Green (dlg@kyubi.co.uk)
# Copyright 2017 Kyubi Systems
# Licensed under the Apache License, Version 2.0 (see LICENSE)
# ------------------------------------------------------------
# 
# ZONECSV 
# 
# Take master grid file generated by makemastergrid, and one or 
# more input NAME files, and calculate concentration sums per 
# zone defined in master grid. Output zone sum data as a CSV file.
#
# Requires supporting libraries in namereader/.
#
# EXAMPLES:
# 
# zonecsv.py --help
# zonecsv.py -d [input dir] -g [grid file] -o [output csv file]
#

import argparse
import pandas as pd
import numpy as np
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

print '+++ Starting zonecsv... +++'

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

    if 'grid' in zones.columns:
        zones = zones.drop('grid', 1)

    if 'geometry' in zones.columns:
        zones = zones.drop('geometry', 1)


    for n in sorted(files):

        # Instantiate NAME object from file
        namefile = name.Name(n)
        timestamps = namefile.timestamps
        namedata = namefile.data
        print "Loaded NAME file %s..." % n

        foo = namedata.join(zones, how='inner')

        for t in timestamps:
            print "Processing time %s..." % t

            totals = {s: (foo[s] * foo[t]).sum() for s in shortnames}

            sum_conc = sum(totals.values())
        
            percents = {'pc_'+s: (totals[s] / sum_conc) * 100.0 for s in shortnames}

            row = util.merge_dicts({"Timestamp": t}, totals, percents)

            writer.writerow(row)

print "Done!"
