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
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QDialog, QApplication, QWidget
from PyQt5.QtCore import pyqtSlot, Qt

from Core.ProcessingTools.rasterLayer import RasterLayer
from Core.Terrain.terrain import Terrain
from Core.DatabaseTools.DatabaseManager.SupportedDrivers.sqliteDatabase import SqliteDatabase
from Settings.settings import Settings

FORMCLASS, _ = uic.loadUiType(os.path.join(
                                   os.path.dirname(__file__),
                                   'gui', 'CustomWidgets',  'mainWindow.ui'
                                   )
                            )

class MainWindow(QMainWindow, FORMCLASS):
       def __init__(self):
              super(MainWindow, self).__init__()
              self.setupUi(self)
              self.raster = RasterLayer()
              self.terrain = Terrain()

       @pyqtSlot(bool, name='on_demPushButton_clicked')
       def setDem(self):
              """
              Sets DEM to visualizer.
              """
              fd = QFileDialog()
              dem = fd.getOpenFileName(caption=self.tr('Select a DEM raster'), filter=self.tr("Raster (*.png *.tif *.tiff)"))
              dem = dem[0] if isinstance(dem, tuple) else dem
              if dem != "":
                     self.raster = RasterLayer(dem)
                     title = self.tr("Visualization of {0}").format(self.raster.name())
                     self.groupBox.setTitle(title)

       def keyPressEvent(self, e):
              """
              test.
              """
              if e.key() == Qt.Key_M and self.raster.isValid():
                     self.terrain.mayaviPlotter(self.raster)

class Main():
       def __init__(self):
              """
              Class constructor.
              """
              self.settings = Settings()
              self.dlg = MainWindow()

app = Main()
app.dlg.show()
QApplication.instance().exec_()
