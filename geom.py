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

from shapely.ops import transform
from shapely.geometry import Point, Polygon

import pyproj

from functools import partial

# --------------------------------------
# reproject geometry as equal area

def reproj(geom, lat1, lat2):
    geom_proj = transform(
        partial(pyproj.transform, pyproj.Proj(init='EPSG:4326'), pyproj.Proj(proj='aea', lat1=lat1, lat2=lat2)), geom
    )    
    return geom_proj


# --------------------------------------
# calculate covering factor of ESRI shape over grid square (float 0.0 -- 1.0)

def coverfactor(geom, square):
    lat_min = geom.bounds['miny'].min()
    lat_max = geom.bounds['maxy'].max()

    # reproject grid square
    square_proj = reproj(square, lat_min, lat_max)

    cf = 0.0

    # loop over shapes in shapefile
    for g in geom:
    
        # reproject shape
        geo_proj = reproj(g, lat_min, lat_max)
        
        inters = geo_proj.intersection(square_proj)

        cf += (inters.area/square_proj.area)
    
    return cf

# --------------------------------------
def shortname(filename):
    return os.path.splitext(os.path.basename(filename))[0]

