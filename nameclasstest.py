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

from nameclass import Namefile

# instantiate new NAME object
name = Namefile('PML_NAME_output/low5dayPML_20150501.txt')

# get extremal concentration values
(min_conc, max_conc) = name.get_minmax()

print "Minimum concentration: ", min_conc
print "Maximum concentration: ", max_conc

# Generate covering factor column for input ESRI shapefile
print 'Starting covering factor calculation...',
name.get_cover('PML_shapefiles/UK.shp')
print ' done.'

n = name.data['UK']
print n.loc[n != 0.0]
