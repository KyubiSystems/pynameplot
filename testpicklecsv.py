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

import pandas as pd
import csv
from namereader import *

# input NAME filename 
namefile = 'PML_NAME_output/low5dayPML_20150501.txt'

# input zone pickle
pklfile = 'PML.pickle'

# output csv filename
outfile = "testdata2.csv"

# -------------------------------------

# Load zone gridfile
zones = pd.read_pickle(pklfile)

# Instantiate NAME object
name = name.Name(namefile)
timestamps = name.timestamps

columns = list(zones)[3::]
pc_cols = [ 'pc_' + c for c in columns ]

print '---------'

data = name.data

data.set_index(['Longitude', 'Latitude'], inplace=True)
zones.set_index(['Longitude', 'Latitude'], inplace=True)

print data

m = pd.merge(name.data, zones, how='inner')

print m

exit()

with open(outfile, 'w') as csvfile:

    fieldnames = ['Timestamp'] + columns + pc_cols
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
    writer.writeheader()

    for t in timestamps:
        print t

        totals = {}
        precents = {}


