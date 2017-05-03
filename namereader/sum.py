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

from .name import Name
from .fileset import Fileset

class Sum:
      'Class to sum over multiple NAME files'
      
      directory = ''
      files = []
      
      # initialise Sum object with directory path
      def __init__(self, directory):
            
            self.directory = directory
            self.fs = Fileset(directory)

      # Add all NAME files in Fileset
      def sumAll(self):
            self.files = self.fs.getAll()
            self.__addFiles(self.files)

      # Add all NAME files between start and end dates
      def sumBetween(self, start, stop):
            self.files = self.fs.between(start, stop)
            self.__addFiles(self.files)

      # Add NAME files for given week number
      def sumWeek(self, w):
            self.files = self.fs.weeks[w]
            self.__addFiles(self.files)

      # Add NAME files for given month number
      def sumMonth(self, m):
            self.files = self.fs.months[m]
            self.__addFiles(self.files)

      # Add NAME files for given year
      def sumYear(self, y):
            self.files = self.fs.years[y]
            self.__addFiles(self.files)

      # NAME data add operation method
      # Tagged as private method
      def __addFiles(self, files):
            
            n = Name(files[0])
            n.add_all()

            m = n.trimmed()
            m = m.rename(columns={'subtotal': 'total'})

            for f in files[1::]:
                  print 'Loading: ', f
                  n2 = Name(f)
                  n2.add_all()
                  m2 = n2.trimmed()

                  m = m.join(m2, how='outer')
                  m = m.fillna(0)

                  m.total = m.total + m.subtotal
                  m = m.drop('subtotal', 1)

            return m

