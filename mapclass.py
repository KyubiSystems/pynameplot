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

    lon_bounds = []
    lat_bounds = []

    def __init__(self, name):

        # 'name' must be a loaded Name object containing parsed data
        
        print 'Plotting figure...',

        # initialise plot
        self.fig, self.ax = plt.subplots()
        self.ax.set_aspect('equal')

        # set default normalisation
        self.norm = matplotlib.colors.LogNorm(vmin=name.min_conc, vmax = name.max_conc, clip=False)

    #--------------
    def draw(self):
        self.m = Basemap(llcrnrlon=lon_bounds[0], llcrnrlat=lat_bounds[0],
                         urcrnrlon=lon_bounds[1], urcrnrlat=lat_bounds[1],
                         projection='cyl', lat_1=45., lat_2=55., lon_0=0.,
                         resolution='l', area_thresh=1000.)
        
        self.m.drawcoastlines(color='white', zorder=8)
        self.m.drawcountries(color='white', zorder=8)
        self.m.drawmapboundary(fill_color='#444444')
        self.m.fillcontinents(color='#bbbbbb', lake_color='#444444')
        self.m.drawparallels(self.lat_axis, linewidth=0.5, color='white', labels=[1, 0, 0, 1], zorder=8)
        self.m.drawmeridians(self.lon_axis, linewidth=0.5, color='white', labels=[1, 0, 0, 1], zorder=8)

        self.ax.set_title(filename, fontsize=10)

    #--------------
    def zoneread(self):

        patches = []
        
        for shapefile in files:
            
            # read ESRI shapefile into GeoPandas object
            shape = gpd.GeoDataFrame.from_file(shapefile)
            
            for poly in shape.geometry:
                if poly.geom_type == 'Polygon':
                    mpoly = transform(m, poly)
                    patches.append(PolygonPatch(mpoly))
                elif poly.geom_type == 'MultiPolygon':
                    for subpoly in poly:
                        mpoly = transform(m, subpoly)
                        patches.append(PolygonPatch(mpoly))
                    
    #-------------
    def zoneplot(self):
        pc = PatchCollection(patches, match_original=True)
        pc.set_facecolor(colors)
        pc.set_edgecolor('red')
        pc.set_alpha(0.5)
        pc.set_linewidth(0.5)
        pc.set_zorder(4)
        
        sq = self.ax.add_collection(pc)
        
        pc2 = PatchCollection(patches, match_original=True)
        pc2.set_facecolor('none')
        pc2.set_edgecolor('red')
        pc2.set_alpha(0.5)
        pc2.set_linewidth(0.5)
        pc2.set_zorder(10)
        
        sq2 = self.ax.add_collection(pc2)

    #--------------
    def grid(self):
        gpatches = []
        
        for poly in self.name['grid']: # TODO: can we do this in parallel? Check operation of transform on columns
            mpoly = transform(m, poly)
            gpatches.append(PolygonPatch(mpoly))
            
    #--------------
    def gridcolormap(self, colormap=cm.rainbow):

        gpc = PatchCollection(gpatches, cmap=colormap, norm=norm, match_original=True)
        gpc.set_edgecolor('none')

    #--------------        
    def gridts(self, ts):
        gpc.set_zorder(6)
        
        gpc.set(array=self.name[ts])
        
        gsq = self.ax.add_collection(gpc)

        self.fig.colorbar(gpc, label=r'Concentration (g s/m$^3$)', shrink=0.7)

    #--------------
    def text(self):
        fig.text(0.4, 0.15, ts, color='white', transform=ax.transAxes)

    #--------------
    def marker(self, lon, lat):
        # plot site marker
        x, y = m(lon, lat)
        self.m.plot(x, y, 'kx', markersize=8, zorder=10)

    #--------------
    def save(self, filename):
        self.fig.savefig(flename, dpi=300)

    #--------------
