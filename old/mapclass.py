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

# plotting libraries
from mpl_toolkits.basemap import Basemap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.collections import PatchCollection

from shapely.ops import transform
from shapely.geometry import Point, Polygon
from descartes import PolygonPatch

# suppress matplotlib/basemap warnings
import warnings
warnings.filterwarnings("ignore")

#--------------
class Map(object):

    "NAME plot base class"

    lon_range = []
    lat_range = []
    conc = []
    projection = 'cyl'  # default projection is cylindrical

    def __init__(self, name):

        # 'name' must be a loaded Name object containing parsed data
        
        print 'Plotting figure...',

        # initialise plot
        self.fig, self.ax = plt.subplots()
        self.ax.set_aspect('equal')

    def autoScale(self):
        # set default normalisation from name file extrema
        self.norm = matplotlib.colors.LogNorm(vmin=name.min_conc, vmax = name.max_conc, clip=False)

    def setScale(self, conc):
        # set manual normalisation
        if not (len(conc) == 2):
            raise 'Invalid concentration range array'

        self.conc = conc
        self.norm = matplotlib.colors.LogNorm(vmin=self.conc[0], vmax=self.conc[1], clip=False)

    def setBounds(self, lon_range, lat_range):
        # set map bounds (arrays)
        if not (len(lon_range) == 2 and len(lat_range) == 2):
            raise 'Invalid longitude/latitude range'

        self.lon_range = lon_range
        self.lat_range = lat_range

    def setAxes(self, lon_axis, lat_axis):
        # set axis tick arrays
        # TODO: should be a sensible default here?
        if not (isinstance(lon_axis, list) and isinstance(lat_axis, list)):
            raise 'Invalid longitude/latitude axis array'

        self.lon_axis = lon_axis
        self.lat_axis = lat_axis

    def setProjection(self, projection='cyl'):
        # set projection (default is cylindrical)
        self.projection = projection

    #--------------
    def drawBase(self):
        # draw base map layers
        self.m = Basemap(llcrnrlon=self.lon_range[0], llcrnrlat=self.lat_range[0],
                         urcrnrlon=self.lon_range[1], urcrnrlat=self.lat_range[1],
                         projection=self.projection, lat_1=45., lat_2=55., lon_0=0.,
                         resolution='l', area_thresh=1000.)
        
        self.m.drawcoastlines(color='white', zorder=8)
        self.m.drawcountries(color='white', zorder=8)
        self.m.drawmapboundary(fill_color='#444444')
        self.m.fillcontinents(color='#bbbbbb', lake_color='#444444')
        self.m.drawparallels(self.lat_axis, linewidth=0.5, color='white', labels=[1, 0, 0, 1], zorder=8)
        self.m.drawmeridians(self.lon_axis, linewidth=0.5, color='white', labels=[1, 0, 0, 1], zorder=8)

        self.ax.set_title(filename, fontsize=10)

    #--------------
    def zoneLoad(self, files):
        # load zones from ESRI shapefiles
        self.patches = []
        
        if not (isinstance(files, list)):
            raise 'invalid list of shapefiles'

        for shapefile in files:
            
            # read ESRI shapefile into GeoPandas object
            shape = gpd.GeoDataFrame.from_file(shapefile)
            
            for poly in shape.geometry:
                if poly.geom_type == 'Polygon':
                    mpoly = transform(m, poly)
                    self.patches.append(PolygonPatch(mpoly))
                elif poly.geom_type == 'MultiPolygon':
                    for subpoly in poly:
                        mpoly = transform(m, subpoly)
                        self.patches.append(PolygonPatch(mpoly))
                    
    #-------------
    def zoneColour(self, colours):

        self.colours = colours

        if not (isinstance(self.colours, list)):
            raise 'Invalid list of zone colours'

        pc = PatchCollection(self.patches, match_original=True)
        pc.set_facecolor(self.colours)
        pc.set_edgecolor('none')
        pc.set_alpha(0.5)
        pc.set_linewidth(0.5)
        pc.set_zorder(4)
        
        sq = self.ax.add_collection(pc)

    def zoneLines(self, edgecolour='red'):        

        pc2 = PatchCollection(self.patches, match_original=True)
        pc2.set_facecolor('none')
        pc2.set_edgecolor(edgecolour)
        pc2.set_alpha(0.5)
        pc2.set_linewidth(0.5)
        pc2.set_zorder(10)
        
        sq2 = self.ax.add_collection(pc2)

    #--------------
    def gridSetup(self):
        # set up data grid

        self.gpatches = []
        
        for poly in self.name['grid']: # TODO: can we do this in parallel? Check operation of transform on columns
            mpoly = transform(m, poly)
            self.gpatches.append(PolygonPatch(mpoly))
            
    #--------------
    def gridColormap(self, colormap=cm.rainbow):
        # set colourmap with predefined normalisation

        self.colormap=colormap
        self.gpc = PatchCollection(self.gpatches, cmap=self.colormap, norm=self.norm, match_original=True)

    def gridSolid(self, colour='blue'):
        # set solid colour

        self.gpc = PatchCollection(self.gpatches, match_original=True)
        self.gpc.set_facecolor(colour)

    def setColumn(self, column='sum'):
        # TODO: check if column exists in name object
        self.column=column

    #--------------        
    def gridDraw(self):

        self.gpc.set_edgecolor('none')
        self.gpc.set_zorder(6)
        self.gpc.set(array=self.name[self.column])
        gsq = self.ax.add_collection(self.gpc)
        self.fig.colorbar(self.gpc, label=r'Concentration (g s/m$^3$)', shrink=0.7)

    #--------------
    def addTimestamp(self):

        self.fig.text(0.4, 0.15, self.column, color='white', transform=self.ax.transAxes)

    #--------------
    def addMarker(self, lon, lat):
        # plot site marker
        x, y = self.m(lon, lat)
        self.m.plot(x, y, 'kx', markersize=8, zorder=10)

    #--------------
    def saveFile(self, filename='plotname.png'):

        self.fig.savefig(flename, dpi=300)

    #--------------