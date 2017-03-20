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

# data frame libraries
import numpy as np
import pandas as pd
import geopandas as gpd

from shapely import speedups
from shapely.geometry import Point, Polygon

import os

# local NAME libraries
from grid import gridsquare
from header import loadheader
from geom import reproj, coverfactor

from shapeclass import Shape

class Namefile:
    'Base class for NAME data storage objects'

    filename = ""
    timestamps = []  
    header = {}  

    # Initialise NAME object from data file at 'filename'
    def __init__(self, filename):
        self.filename = filename

        if not os.path.isfile(self.filename):
            exit('Input filename ' + self.filename + ' does not exist')

        # Enable Shapely native C++ acceleration
        if speedups.available:
            speedups.enable()

        # read and parse NAME file header
        self.header = loadheader(self.filename)

        # get grid size from header
        delta_lon = float(self.header['X grid resolution'])
        delta_lat = float(self.header['Y grid resolution'])
        self.grid_size = (delta_lon, delta_lat)

        # read CSV portion of NAME file into pandas DataFrame
        df = pd.read_csv(self.filename, header=31)

        # Clear bad (empty) data columns from DataFrame
        df = df.dropna(axis=1, how='all')
    
        # Get column header timestamp names from first row
        c = map(list, df[0:1].values)
        collist = c[0]
    
        # Set leader column names
        collist[1:4] = ['X-Index', 'Y-Index', 'Longitude', 'Latitude']
        collist = [ x.strip() for x in collist ]
    
        # Get observation timestamp strings
        self.timestamps = collist[5::]
    
        # Apply labels to DataFrame
        df.columns = collist[1::]
    
        # Drop leading rows
        df = df.drop([0,1,2,3])
    
        # Convert strings to floats where possible
        df = df.apply(lambda x: pd.to_numeric(x, errors='ignore'))
    
        # Set mapping coordinate for GeoDataFrame
        crs = {'init': 'epsg:4326'}
    
        # Generate Shapely Point objects for each grid point
        #df['points'] = [ Point(xy) for xy in zip(df.Longitude, df.Latitude) ]
    
        # Generate Shapely Polygons for grid squares
        df['grid'] = [ Polygon(gridsquare(xy + self.grid_size)) for xy in zip(df.Longitude, df.Latitude) ]
    
        # Create GeoDataFrame with point and grid geometry columns
        self.data = gpd.GeoDataFrame(df, crs=crs, geometry=df['grid'])


    # sum given list of timestamp columns
    def add_range(self, ts):
        self.data['total'] = self.data[ts].sum(axis=1)


    # sum all timestamp columns in file
    def add_all(self):
        self.data['total'] = self.data[self.timestamps].sum(axis=1)


    # Get minimum & maximum concentration values
    def get_minmax(self):
        # Flatten list of concentration values
        cl = self.data[self.timestamps].values.tolist()
        flat = [item for sublist in cl for item in sublist]

        # Get minimum concentration value
        self.min_conc = min([x for x in flat if x > 0.0])

        # Get maximum concentration value
        self.max_conc = self.data[self.timestamps].values.max()
        
        return (self.min_conc, self.max_conc)

        
    # Get covering factor value column for input ESRI shapefile
    def get_cover(self, shapefile):

        shape = Shape(shapefile)

        # calculate covering factor column
        self.data[shape.shortname] = [coverfactor(shape.proj_geo, s, shape.lat_min, shape.lat_max) for s in self.data['grid']]
        
