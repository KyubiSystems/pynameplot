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

import geopandas as gpd
import os

from geom import reproj

class Shape(object):
    'Base class for shape derived from ESRI shapefile'

    shapefile = ""
    shortname = ""

    # Initialise shape object from ESRI file at 'filename'
    def __init__(self, shapefile):
        self.shapefile = shapefile
        
        if not os.path.isfile(self.shapefile):
            exit('Input shapefile ' + self.shapefile + ' does not exist')

        self.shortname = self.shorten(self.shapefile)

        shp = gpd.GeoDataFrame.from_file(self.shapefile)

        self.geo = shp.geometry

        # Get shape latitude extent
        self.lat_min = self.geo.bounds['miny'].min()
        self.lat_max = self.geo.bounds['maxy'].max()

        # reprojected geometry
        self.proj_geo = [ reproj(g, self.lat_min, self.lat_max) for g in self.geo ]
        
    def shorten(self, filename):
        return os.path.splitext(os.path.basename(filename))[0]
