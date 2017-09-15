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

# --------------------------------------
def coverfactor(geom, square):
    """
    Calculate covering factor of ESRI shape over grid square.
    Value is float in range 0.0 -- 1.0

    geom -- Shapely geometry
    square -- Shapely geometry of grid square
    lat_min -- reference latitude 1
    lat_max -- reference latitude 2
    """

    cf = 0.0

    # geometry of intersection between input shape and grid square
    inters = geom.intersection(square)
        
    # ratio of areas is covering factor
    cf += (inters.area/square.area)
    
    return cf


# --------------------------------------
def gridsquare(coords):
    """
    Generate list of coordinates for gridsquare
    coords -- 4-tuple of grid centre coords, dlongitude, dlatitude
    
    returns list of 4 (lon, lat) coords for grid corners
    """

    (lon, lat, dlon, dlat) = coords
    gs = [(lon - dlon/2., lat - dlat/2.), (lon - dlon/2., lat + dlat/2.), (lon + dlon/2., lat + dlat/2.), (lon + dlon/2., lat - dlat/2.)]
    return gs
