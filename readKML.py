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

from fastkml import kml

# Create the KML object to store the parsed result
k = kml.KML()

with open('kmz_old/doc.kml', 'r') as kmlfile:
     data = kmlfile.read()

     k.from_string(data)

     features = list(k.features())

     f = features[0].features()
     
     f2 = list(f)

     print len(f2)
     
     print f2[0]
     print f2[0].name
     print f2[0].description

     f3 = list(f2[0].features())
     print f3

