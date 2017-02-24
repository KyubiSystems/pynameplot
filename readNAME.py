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
from geopandas import GeoDataFrame
from shapely.geometry import Point

filename = '1daysurfaceWARRI_20110715.txt'

# read CSV portion of NAME file into pandas DataFrame
df = pd.read_csv(filename, header=31)

# Get column header timestamp names from first row
c = map(list, df[0:1].values)
collist = c[0]

# Set leader column names
collist[1:4] = ['X-Index', 'Y-Index', 'Longitude', 'Latitude']

# Apply labels to DataFrame
df.columns = collist[1::]

# Drop leading rows
df = df.drop([0,1,2,3])

# Convert strings to floats where possible
df = df.apply(lambda x: pd.to_numeric(x, errors='ignore'))

# Clear bad (empty) data columns from DataFrame
df = df.dropna(axis=1, how='all')

# Set mapping coordinate
crs = {'init': 'epsg:4326'}

# Generate Shapely Point objects for each grid point
geometry = [Point(xy) for xy in zip(df.Longitude, df.Latitude)]
geo_df = GeoDataFrame(df, crs=crs, geometry=geometry)

print geo_df
