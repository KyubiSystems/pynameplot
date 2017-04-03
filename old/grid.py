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

# Generate list of coordinates for gridsquare
# input 4-tuple of grid centre, dlongitude, dlatitude
# return list of 4 coords for grid corners

def gridsquare(coords):
    (lon, lat, dlon, dlat) = coords
    gs = [(lon - dlon/2., lat - dlat/2.), (lon - dlon/2., lat + dlat/2.), (lon + dlon/2., lat + dlat/2.), (lon + dlon/2., lat - dlat/2.)]
    return gs
