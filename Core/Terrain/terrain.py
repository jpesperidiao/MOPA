# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MOPA
                                 An independet project
 Método de Obtenção da Posição de Atirador
                              -------------------
        begin                : 2018-01-13
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
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D
from PyQt5.QtCore import QObject

class Terrain(QObject):
    def __init__(self):
        """
        Class constructor.
        """
        super(Terrain, self).__init__()

    def defaultPlottingParameters(self):
        """
        Gets default parameters for plotting an array.
        :return: (dict) plotting parameters map.
        """
        return {
            'rowStride' : 10,
            'colStride' : 10,
            'initialCol' : 0,
            'finalCol' : 1000,
            'initialRow' : 0,
            'finalRow' : 1000,
            'cmap' : cm.YlGnBu,
            'linewidth' : 0,
            'antialiased' : False,
            'shrink' : .5,
            'aspect' : 5,
            'alpha' : .0
        }

    def plotter(self, elevation, points=None, parameters=None):
        """
        Generates a 3D plotting object.
        :param elevation: (Numpy.ndarray) terrain's elevation band as a numpy array.
        :param points: (list-of-Numpy.ndarray) list of points to be plotted over the terrain.
        :param parameters: (dict) plotting parameters.
        """
        if parameters is None:
            parameters = self.defaultPlottingParameters()
        fig = plt.figure()
        ax = Axes3D(fig)
        Z = elevation[
                parameters['initialCol']:parameters['finalCol'],\
                parameters['initialRow']:parameters['finalRow']
            ]
        X = np.arange(parameters['initialCol'], parameters['finalCol'])
        Y = np.arange(parameters['initialRow'], parameters['finalRow'])
        X,Y = np.meshgrid(X,Y)
        surf = ax.plot_surface(X, Y, Z, rstride=parameters['rowStride'], cstride=parameters['colStride'],\
                    cmap=parameters['cmap'], linewidth=parameters['linewidth'], antialiased=parameters['antialiased']
                )
        fig.colorbar(surf, shrink=parameters['shrink'], aspect=parameters['aspect'], alpha=parameters['alpha'])
            
        ax.zaxis.set_major_locator(LinearLocator(10))
        ax.zaxis.set_major_formatter(FormatStrFormatter('%.08f'))    
        if points is not None:
            #ax.scatter(vet[:,0], vet[:,1], vet[:,4], c='blue')
            ax.scatter(points[:,0], points[:,1], points[:,4], c='cyan')

        ax.set_xlabel(self.tr('Column'))
        ax.set_ylabel(self.tr('Row'))
        ax.set_zlabel(self.tr('Height'))
        plt.show()
        return fig
