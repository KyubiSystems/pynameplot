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
import itertools

from .name import Name
from .util import basename

class Fileset:
      'Class to sum across multiple NAME files'

      directory = ''
      files = []
      dates = {}
      start = ''
      finish = ''
      mode = ''  # one of day|week|month|year|all
      valid_modes = ['day', 'week', 'month', 'year', 'all']

      # initialise Fileset object with directory path
      def __init__(self, directory):

            self.directory = directory

            if not os.path.isdir(directory):
                  raise ValueError

            self.files = glob.glob(directory + '/*.txt')

            for f in self.files:
                self.dates[basename(f)] = arrow.get(basename(f), 'YYYYMMMDD')  


      def setmode(self, mode):

            if mode not in self.valid_modes:
                  raise ValueError

            self.mode = mode

