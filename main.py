# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MOPA
                                 An independet project
 Método de Obtenção da Posição de Atirador
                              -------------------
        begin                : 2018-12-21
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

from Core.ProcessingTools.rasterLayer import RasterLayer
from Core.Terrain.terrain import Terrain

path = '/Users/Joao/Documents/Projetos/MOPA/.dev/testing_data/ASTGTM2_N39W096/ASTGTM2_N39W096_num.tif'
rl = RasterLayer(path)
t = Terrain()
param = t.defaultPlottingParameters()
param['initialRow'] = 1000
param['finalRow'] = 1500
param['initialCol'] = 1000
param['finalCol'] = 1500
t.plotter(rl, parameters=param)
print(t)