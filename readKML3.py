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

from pykml import parser
from ast import literal_eval
from shapely.geometry.polygon import LinearRing


with open('kmz_old/doc.kml','r') as kml:
     k = parser.parse(kml).getroot().Document.Folder

for pm in k.iterdescendants():

     if hasattr(pm, 'LinearRing'):
          coords = pm.LinearRing.coordinates.text
          coords_list = coords.split(" ")
          coords_list = filter(None, coords_list)

          geom = []
          for c in coords_list:
               geom.append(literal_eval(c))

#          print geom

          lr = LinearRing(geom)
          print lr
