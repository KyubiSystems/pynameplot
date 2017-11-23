#!/usr/bin/env python

import pandas as pd
import numpy as np
import csv

from namereader import *

z = '/data/name/NAME_data/NAME_plotting/PKL/WAO_mastergrid.pkl'
f = '/data/name/NAME_data/NAME_plotting/NAME_data/1column_test_data/lowWAO_C1_T1_201201010000.txt'

zones = pd.read_pickle(z)
zones = zones.to_dense()
zones = zones.fillna(0)

if 'grid' in zones.columns:
    zones = zones.drop('grid', 1)
    
if 'geometry' in zones.columns:
    zones = zones.drop('geometry', 1)

print 'Loaded grid file...'

namefile = name.Name(f)
timestamps = namefile.timestamps
namedata = namefile.data

print 'Loaded data...'

print timestamps

print zones.columns
print namedata.columns

foo = namedata.join(zones, how='inner')

print foo

