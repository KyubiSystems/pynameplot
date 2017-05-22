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


class Map(object):

    """
    Define and create a visualisation plot
    from NAME concentration data
    """

    lon_range = []
    lat_range = []
    lon_axis = []
    lat_axis = []

    conc = []

    def __init__(self, name, column='total'):
        """
        Initialise Map object.

        name   -- a loaded Name object containing parsed data
        column -- column name to plot. Default is 'total' column from summed file.

        Default is to set auto-scale normalisation from 
        extremal values of input data.
        """
        
        self.name = name
        self.column = column
        self.fig, self.ax = plt.subplots()
        self.ax.set_aspect('equal')
        self.solid = False

        # set default projection to cylindrical
        self.projection = 'cyl'

        # set default fixed scale normalisation for output plot
        self.setFixedScale()


    def setFixedScale(self, conc=(5.e-9, 1.e-4)):
        """
        Set fixed scale normalisation manually.

        conc -- 2-tuple containing (min, max) values of concentration scale
        """

        if not (len(conc) == 2):
            raise ValueError('Invalid concentration range array')

        self.norm = matplotlib.colors.LogNorm(vmin=conc[0], vmax=conc[1], clip=False)

    def setAutoScale(self, column=self.column):
        """
        Set autoscale normalisation.

        column -- Name of data column to extract (min, max) values for scale normalisagtion
        """

        self.name.get_minmax(column)

        # set default normalisation from name file extrema
        self.norm = matplotlib.colors.LogNorm(vmin=self.name.min_conc, vmax=self.name.max_conc, clip=False)

    def setBounds(self, lon_range, lat_range):
        """
        Set map latitude and longitude bounds.

        lon_range -- 2-tuple containing (lon_min, lon_max)
        lat_range -- 2-tuple containing (lat_min, lat_max)
        """

        if not (len(lon_range) == 2 and len(lat_range) == 2):
            raise ValueError('Invalid longitude/latitude range')

        self.lon_range = lon_range
        self.lat_range = lat_range

    def setAxes(self, lon_axis, lat_axis):
        """
        Set map tick arrays in longitude and latitude.

        lon_axis -- list containing longitude tick mark values.
        lat_axis -- list containing latitude tick mark values.
        """

        if not (isinstance(lon_axis, list) and isinstance(lat_axis, list)):
            raise ValueError('Invalid longitude/latitude axis array')

        self.lon_axis = lon_axis
        self.lat_axis = lat_axis

    def setProjection(self, projection):
        """
        Override default projection type.

        projection -- string giving projection type
        """

        self.projection = projection

    # --------------------------------------------------------
    def drawBase(self, caption, fontsize=10):
        """
        Set up map projection
        Draw basic map layout including coastlines and boundaries
        Draw lat-long grid
        Set plot title from filename
        """

        self.m = Basemap(llcrnrlon=self.lon_range[0], llcrnrlat=self.lat_range[0],
                         urcrnrlon=self.lon_range[1], urcrnrlat=self.lat_range[1],
                         projection=self.projection, lat_1=45., lat_2=55., lon_0=0.,
                         resolution='l', area_thresh=1000.)
        
        self.m.drawcoastlines(color='white', linewidth=0.6, zorder=8)
        self.m.drawcountries(color='white', zorder=8)
        self.m.drawmapboundary(fill_color='#444444')
        self.m.fillcontinents(color='#bbbbbb', lake_color='#444444')
        self.m.drawparallels(self.lat_axis, linewidth=0.3, color='white', labels=[1, 0, 0, 1], zorder=8, fontsize=5)
        self.m.drawmeridians(self.lon_axis, linewidth=0.3, color='white', labels=[1, 0, 0, 1], zorder=8, fontsize=5)

        self.ax.set_title(caption, fontsize=fontsize)

    # --------------------------------------------------------
    def zoneLoad(self, files):
        """
        Load gepgraphic zones from list of ESRI shapefiles
        files -- list containing ESRI shapefiles
        """

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
                    
    def zoneColour(self, colours):
        """
        Set display colours for defined ESRI shapes
        colours -- list containing HTML colour names
        """

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
        """
        Set boundary colour for defined ESRI shapes
        edgecolour -- HTML colour name for boundary
        """

        pc2 = PatchCollection(self.patches, match_original=True)
        pc2.set_facecolor('none')
        pc2.set_edgecolor(edgecolour)
        pc2.set_alpha(0.5)
        pc2.set_linewidth(0.5)
        pc2.set_zorder(10)
        
        sq2 = self.ax.add_collection(pc2)

    # --------------------------------------------------------
    def setColormap(self, colormap='rainbow'):
        """
        Set colourmap with existing normalisation
        colormap -- Matplotlib colourmap name
        """
        self.colormap = getattr(cm, colormap)

    def drawSolid(self, column, color='blue', zorder=6):
        """
        Draw solid shape showing extent of conc > 0.0
        color -- HTML colour
        """
        self.solid = True

        mesh = self.name.data[column]
        mesh1 = mesh.loc[mesh > 0.0]

        mesh2 = mesh1.unstack(level=1)
        mesh2 = mesh2.fillna(0)

        lons = mesh2.index.get_level_values('Longitude')
        lats = mesh2.columns

        mesh2 = mesh2.transpose()

        mesh2[mesh2 > 0] = 1.0
        mesh3 = mesh2.mask(mesh2 > 0)

        x,y = self.m(lons, lats)

        cmap = matplotlib.colors.ListedColormap([color])
        norm = matplotlib.colors.LogNorm(vmin=0.99, vmax=1.0, clip=False)

        self.m.pcolormesh(x, y, mesh3, norm=norm, cmap=cmap, zorder=zorder)


    def drawMesh(self, column, zorder=6):
        """
        Draw data column values on map
        Add colourbar to plot where plot is not solid type
        """
        mesh = self.name.data[column]
        mesh1 = mesh.loc[mesh > 0.0]

        mesh2 = mesh1.unstack(level=1)
        mesh2 = mesh2.fillna(0)

        lons = mesh2.index.get_level_values('Longitude')
        lats = mesh2.columns

        mesh2 = mesh2.transpose()

        x,y = self.m(lons, lats)

        self.m.pcolormesh(x, y, mesh2, cmap=self.cmap, norm=self.norm, zorder=zorder)

        if not self.solid:
            self.fig.colorbar(self.gpc, label=r'Concentration (g s/m$^3$)', shrink=0.5)

    # --------------------------------------------------------
    def addTimestamp(self):
        """
        Add timestamp to plot
        """
        self.fig.text(0.4, 0.15, self.column, color='white', transform=self.ax.transAxes)

    def addMarker(self, lon, lat):
        """
        Add marker to plot at station coordinates
        lon -- station longitude
        lat -- station latitude
        """
        x, y = self.m(lon, lat)
        self.m.plot(x, y, 'kx', markersize=4, zorder=10)

    def saveFile(self, filename='plotname.png'):
        """
        Save plot output file
        filename -- output file including type extension
        """
        self.fig.savefig(filename, dpi=300)

    # --------------------------------------------------------
