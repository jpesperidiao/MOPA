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

import os

from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QDialog, QWidget

from Core.ProcessingTools.rasterLayer import RasterLayer
from Core.Terrain.terrain import Terrain

FORMCLASS, _ = uic.loadUiType(os.path.join(
                                   os.path.dirname(__file__),
                                   'mainWindow.ui'
                                   )
                            )

class MainWindow(QMainWindow, FORMCLASS):
       def __init__(self):
              super(MainWindow, self).__init__()
              self.setupUi(self)
              self.raster = RasterLayer()
              self.terrain = Terrain()
              self.visualizePushButton.setEnabled(False)

       @pyqtSlot(bool, name='on_demPushButton_clicked')
       def setDem(self):
              """
              Sets DEM informations to GUI and prepares it for visualization.
              """
              fd = QFileDialog()
              dem = fd.getOpenFileName(caption=self.tr('Select a DEM raster'), filter=self.tr("Raster (*.png *.tif *.tiff)"))
              dem = dem[0] if isinstance(dem, tuple) else dem
              self.visualizePushButton.setEnabled(self.raster is not None)
              if dem != "":
                     self.raster.setRaster(dem)
                     self.visualizePushButton.setEnabled(self.raster.isValid())
                     self.groupBox.setTitle(self.tr("DEM information: {0}").format(self.raster.name()))
                     self.fileLabel.setText(self.tr("File path: {0}").format(dem))
                     self.crsLabel.setText(self.tr("CRS name: {0}").format(self.raster.projection()))
                     self.maxLabel.setText(self.tr("Max. altitude: {0} m").format(self.raster.bands().max()))
                     self.minLabel.setText(self.tr("Min. altitude: {0} m").format(self.raster.bands().min()))
                     self.heightLabel.setText(self.tr("Raster height: {0}").format(self.raster.height()))
                     self.widthLabel.setText(self.tr("Raster width: {0}").format(self.raster.width()))
                     reso =  self.tr("Spatial resolution: {0} m (detected)") if not self.raster.isGeographic()\
                             else self.tr("Spatial resolution: {0} m (detected)")
                     self.resLabel.setText(reso.format(self.raster.spatialResolution()))
                     units = "meters" if not self.raster.isGeographic() else "degrees"
                     self.unitsLabel.setText(self.tr("DEM units: {0}").format(units))

       @pyqtSlot(bool, name='on_visualizePushButton_clicked')
       def visualizeDem(self):
              """
              Produces the visualization for current raster.
              """
              if self.raster.isValid():
                     self.terrain.mayaviPlotter(self.raster)
