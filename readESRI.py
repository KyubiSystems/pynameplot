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

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import geopandas as gpd


shapefile = "PML_shapefiles/North_sea.shp"
base = os.path.basename(shapefile)
region = os.path.splitext(base)[0]

print region

shp = gpd.read_file(shapefile)

fig, ax = plt.subplots()

ax.set_aspect('equal')

shp.plot(ax=ax, color='blue')

ax.set_title(region, fontsize=20)

pngfile = region + '.png'
fig.savefig(pngfile, dpi=300)
