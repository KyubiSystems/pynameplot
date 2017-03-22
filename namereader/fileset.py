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
from itertools import groupby

from .name import Name
from .util import shortname

class Fileset:
      'Class to sum across multiple NAME files'

      directory = ''
      files = []
      mode = ''  # one of day|week|month|year|all
      valid_modes = ['day', 'week', 'month', 'year', 'all']

      dates = {}
      weeks = {}
      months = {}
      years = {}


      # initialise Fileset object with directory path
      def __init__(self, directory):

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


      # select Fileset mode for subsequent processing
      def setmode(self, mode):

            if mode not in self.valid_modes:
                  raise ValueError

            self.mode = mode

      # return ISO-8601 week number from Arrow object
      def getWeek(self, a):
            return a.isocalendar()[1]

      # return month number from Arrow object
      def getMonth(self, a):
            return a.format('M')

      # return 4-digit year from Arrow object
      def getYear(self, a):
            return a.format('YYYY')
