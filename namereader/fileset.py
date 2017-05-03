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

import arrow
import glob
import os
from collections import defaultdict

from .name import Name
from .util import shortname

class Fileset:
      """Read directory of NAME files, 
      extract subset corresponding to given time period
      """
      directory = ''
      files = []

      dates = {}
      weeks = defaultdict(list)
      months = defaultdict(list)
      years = defaultdict(list)

      def __init__(self, directory):
            """Initialise Fileset object.

            directory -- input directory path
            """
            self.directory = directory

            if not os.path.isdir(directory):
                  raise ValueError

            self.files = glob.glob(directory + '/*.txt')

            # group input filenames by week, month, year
            # generate dict of lists
            for f in self.files:
                  
                  g = shortname(f)
                  d = arrow.get(g, 'YYYYMMDD')
                  
                  self.dates[g] = d

                  self.weeks[self.getWeek(d)].append(f)
                  self.months[self.getMonth(d)].append(f)
                  self.years[self.getYear(d)].append(f)


      def getAll(self):
            """Return all NAME files found in directory"""
            return self.files


      def between(self, start, stop):
            """Return NAME files between two dates

            start -- start date, YYYYMMDD format
            stop -- stop date, YYYYMMDD format
            """
            a = arrow.get(start, 'YYYYMMDD')
            b = arrow.get(stop, 'YYYYMMDD')
            result = []
            for f in self.files:
                  g = shortname(f)
                  d = arrow.get(g, 'YYYYMMDD')
                  if (d >= a) and (d <=b):
                        result.append(f)
            return result


      def getWeek(self, a):
            """Return week number for given Arrow object
            a -- Arrow timestamp object
           """
            return a.isocalendar()[1]


      def getMonth(self, a):
            """Return month number for given Arrow object
            a -- Arrow timestamp object
            """
            return a.format('M')


      def getYear(self, a):
            """Return year for given Arrow object
            a -- Arrow timestamp object
            """

            return a.format('YYYY')
