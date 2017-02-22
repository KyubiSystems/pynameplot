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

filename = '1daysurfaceWARRI_20110715.txt'

header = {}

with open(filename, 'r') as f:

    for line in range(1,19):
        h = f.readline()

        if ":" in h:
            (key, val) = h.split(":",1)
            key = key.strip()
            val = val.strip()

            print 'setting ' + key
            header[key] = val

print header['X grid resolution']

print len(header)
