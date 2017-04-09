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

from shapely.ops import transform, cascaded_union
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

def coverfactor(geom, square, lat_min, lat_max):

    # reproject grid square
    square_proj = reproj(square, lat_min, lat_max)

    cf = 0.0

    # loop over shapes in shapefile

    # for g in geom:

    inters = geom.intersection(square_proj)
        
    cf += (inters.area/square_proj.area)
    
    return cf

# --------------------------------------
# Generate list of coordinates for gridsquare
# input 4-tuple of grid centre, dlongitude, dlatitude
# return list of 4 coords for grid corners

def gridsquare(coords):
    (lon, lat, dlon, dlat) = coords
    gs = [(lon - dlon/2., lat - dlat/2.), (lon - dlon/2., lat + dlat/2.), (lon + dlon/2., lat + dlat/2.), (lon + dlon/2., lat - dlat/2.)]
    return gs


