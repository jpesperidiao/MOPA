# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MOPA
                                 An independet project
 Método de Obtenção da Posição de Atirador
                              -------------------
        begin                : 2019-01-13
        git sha              : $Format:%H$
        copyright            : (C) 2018 by João P. Esperidião
        email                : joao.p2709@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import numpy as np
# import matplotlib
# import matplotlib.pyplot as plt
# from matplotlib import cm
# from matplotlib.ticker import LinearLocator, FormatStrFormatter
# from mpl_toolkits.mplot3d import Axes3D
from mayavi import mlab
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QWidget

class Terrain(QObject):
    def __init__(self):
        """
        Class constructor.
        """
        super(Terrain, self).__init__()

    # def defaultPlottingParameters(self):
    #     """
    #     Gets default parameters for plotting an array.
    #     :return: (dict) plotting parameters map.
    #     """
    #     return {
    #         'rowStride' : 10,
    #         'colStride' : 10,
    #         'initialCol' : 0,
    #         'finalCol' : 1000,
    #         'initialRow' : 0,
    #         'finalRow' : 1000,
    #         'cmap' : cm.gist_earth,
    #         'linewidth' : 0,
    #         'antialiased' : False,
    #         'shrink' : .5,
    #         'aspect' : 5,
    #         'alpha' : .0
    #     }

    # def plotter(self, raster, points=None, parameters=None):
    #     """
    #     Generates a 3D plotting object.
    #     :param raster: (RasterLayer) terrain's DEM raster.
    #     :param points: (list-of-Numpy.ndarray) list of points to be plotted over the terrain.
    #     :param parameters: (dict) plotting parameters.
    #     """
    #     if parameters is None:
    #         parameters = self.defaultPlottingParameters()
    #     fig = plt.figure()
    #     ax = Axes3D(fig)
    #     ax.set_title(self.tr('Visualization from {0}').format(raster.name()))
    #     elevation = raster.bands()
    #     Z = elevation[
    #             parameters['initialCol']:parameters['finalCol'],\
    #             parameters['initialRow']:parameters['finalRow']
    #         ]
    #     X = np.arange(parameters['initialCol'], parameters['finalCol'])
    #     Y = np.arange(parameters['initialRow'], parameters['finalRow'])
    #     X,Y = np.meshgrid(X,Y)
    #     surf = ax.plot_surface(X, Y, Z, rstride=parameters['rowStride'], cstride=parameters['colStride'],\
    #                 cmap=parameters['cmap'], linewidth=parameters['linewidth'], antialiased=parameters['antialiased']
    #             )
    #     fig.colorbar(surf, shrink=parameters['shrink'], aspect=parameters['aspect'], alpha=parameters['alpha'])
            
    #     ax.zaxis.set_major_locator(LinearLocator(10))
    #     ax.zaxis.set_major_formatter(FormatStrFormatter('%.2f'))    
    #     if points is not None:
    #         #ax.scatter(vet[:,0], vet[:,1], vet[:,4], c='blue')
    #         ax.scatter(points[:,0], points[:,1], points[:,4], c='cyan')

    #     ax.set_xlabel(self.tr('Column'))
    #     ax.set_ylabel(self.tr('Row'))
    #     ax.set_zlabel(self.tr('Height'))
    #     plt.show()
    #     return fig

    def mayaviPlotter(self, raster, title=None):
        """
        Creates a 3D view from a raster using Mayavi lib.
        :param raster: (RasterLayer) terrain's DEM raster.
        :param title: (str) title for Scene window.
        """
        # obs.: mayavi interfered on matplotlib's execution (it crashed big time)
        if raster.bandCount() != 1:
            return
        dem = raster.bands()
        x = np.arange(0, raster.width())
        y = np.arange(0, raster.height())
        x, y = np.meshgrid(x, y)
        if title is None:
            title = self.tr("Visualization of {0}").format(raster.name())
        mlab.figure(title)
        mlab.mesh(x, y, dem)
        mlab.show()
        return
