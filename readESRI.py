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

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import geopandas as gpd

filename = "PML_shapefiles/North_sea.shp"

shp = gpd.read_file(filename)

fig, ax = plt.subplots()

ax.set_aspect('equal')

shp.plot(ax=ax, color='blue')

ax.set_title('this is the figure title', fontsize=20)

fig.savefig('foo2.png', dpi=300)
