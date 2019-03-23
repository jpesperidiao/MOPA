# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MOPA
                     An independet project
 Método de Obtenção da Posição de Atirador
                  -------------------
     begin          : 2018-12-21
     git sha        : $Format:%H$
     copyright         : (C) 2018 by João P. Esperidião
     email          : joao.p2709@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                           *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                    *
 *                                           *
 ***************************************************************************/
"""

import os
from time import time
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QMainWindow

from Core.ProcessingTools.rasterLayer import RasterLayer
from Core.Terrain.terrain import Terrain
from Core.Sensor.sensorsManager import SensorsManager
from Core.Observation.observationsManager import ObservationsManager
from Core.ProcessingTools.shooterFinder import ShooterFinder
from Gui.CustomWidgets.summaryDialog import SummaryDialog
from Gui.CustomWidgets.FeatureForms.observationsManagerDialog import ObservationsManagerDialog

FORMCLASS, _ = uic.loadUiType(os.path.join(
                    os.path.dirname(__file__),
                    'mainWindow.ui'
                    )
                )

class MainWindow(QMainWindow, FORMCLASS):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        icon = QIcon(
            os.path.join(os.path.dirname(__file__), '..', '..', 'Icons', 'icon.svg')
        )
        # self.setIcon(icon)
        self.setWindowIcon(icon)
        self.raster = RasterLayer()
        self.terrain = Terrain()
        self.visualizePushButton.setEnabled(False)
        self.setMethods()
        self.setupObservations()
        self.setupSensors()

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
            self.setupSensors()
            self.visualizePushButton.setEnabled(self.raster.isValid())
            self.groupBox.setTitle(self.tr("DEM information: {0}").format(self.raster.name()))
            self.fileLabel.setText(self.tr("File path: {0}").format(dem))
            self.crsLabel.setText(self.tr("CRS name: {0}").format(self.raster.projection()))
            self.maxLabel.setText(self.tr("Max. altitude: {0:.2f} m").format(self.raster.max()))
            self.minLabel.setText(self.tr("Min. altitude: {0:.2f} m").format(self.raster.min()))
            self.heightLabel.setText(self.tr("Raster height: {0}").format(self.raster.height()))
            self.widthLabel.setText(self.tr("Raster width: {0}").format(self.raster.width()))
            reso =  self.tr("Spatial resolution: {0:.2f} m (detected)") if self.raster.isGeographic()\
                 else self.tr("Spatial resolution: {0:.2f} m")
            self.resLabel.setText(reso.format(self.raster.spatialResolution()))
            units = self.tr("meters") if not self.raster.isGeographic() else self.tr("degrees")
            self.unitsLabel.setText(self.tr("DEM units: {0}").format(units))

    @pyqtSlot(bool, name='on_visualizePushButton_clicked')
    def visualizeDem(self):
        """
        Produces the visualization for current raster.
        """
        if self.raster.isValid():
            self.terrain.mayaviPlotter(self.raster)

    def getAllSensorsFromRaster(self, dem):
        """
        Retrieves all sensors inside of a DEM.
        :param dem: (RasterLayer) DEM to be checked for sensors.
        :return: (list-of-Sensor)
        """
        return list(SensorsManager().getSensorsInsideRaster(dem).values())

    def setupSensors(self):
        """
        Sets sensors to GUI.
        """
        if self.raster.isValid():
            self.sensorWidget.refresh(self.getAllSensorsFromRaster(self.raster))
        else:
            self.sensorWidget.refresh(SensorsManager().allSensors().values())

    def getAllObsFromSensor(self, sensor=None):
        """
        Retrieves all observations made from a sensor.
        :param dem: (RasterLayer) DEM to be checked for sensors.
        :return: (list-of-Sensor)
        """
        sensor = sensor or (self.sensorWidget.currentSensor() or \
                 SensorsManager().newSensor())
        if self.sensorWidget.currentSensor().isValid():
            return ObservationsManager().getObservationsFromSensor(
                self.sensorWidget.currentSensor()['id']
            )
        else:
            return ObservationsManager().allObservations()

    def setupObservations(self):
        """
        Sets observations to GUI.
        """
        if self.raster.isValid():
            self.obsWidget.refresh(self.getAllObsFromSensor())
        else:
            self.obsWidget.refresh(ObservationsManager().allObservations().values())

    # @pyqtSlot(int, name='on_obsComboBox_currentIndexChanged')
    # def checkEditingObservation(self):
    #     """
    #     Checks whether current observations may be editted.
    #     """
    #     self.updateObservationPushButton.setEnabled(self.obsComboBox.currentIndex() > 0)

    # @pyqtSlot(bool, name="on_updateObservationPushButton_clicked")
    # def updateObservation(self):
    #     """
    #     [TEST] Updates an observation in the database.
    #     """
    #     if self.obsComboBox.currentIndex() > 0:
    #         obsId = int(self.obsComboBox.currentText().split(" ")[-1])
    #         obs = ObservationsManager().allObservations()[obsId]
    #         ObservationsManagerDialog().openForm(obs)

    # @pyqtSlot(bool, name="on_addObservationPushButton_clicked")
    # def addObservation(self):
    #     """
    #     [TEST] Adds an observation to the database.
    #     """
    #     ObservationsManagerDialog().openForm()

    def methodNameMap(self):
        """
        
        """
        sf = ShooterFinder()
        return {
            sf.Helmert : self.tr("Helmert Algorithm"),
            sf.Analytical : self.tr("Analytical Algorithm"),
            sf.Combined : self.tr("Combined Algorithm")
        }

    def setMethods(self):
        """
        Sets up method options.
        """
        self.methodComboBox.clear()
        algs = list(self.methodNameMap().values())
        algs.insert(0, self.tr("Select an algorithm..."))
        self.methodComboBox.addItems(algs)

    @pyqtSlot(bool, name='on_findPushButton_clicked')
    def findShooter(self):
        """
        
        """
        # interface parameters should be validated here instead of try/except
        try:
            idx = self.methodComboBox.currentIndex()
            if idx > 0 and self.raster is not None and self.raster.isValid():
                obsId = int(self.obsComboBox.currentText().split(" ")[-1])
                obs = ObservationsManager().allObservations()[obsId]
                sid = int(self.sensorComboBox.currentText().split("ID = ")[-1].split(")")[0])
                sensor = SensorsManager().getSensorFromId(sid)
                start = time()
                shooters = ShooterFinder().findShooter(idx - 1, sensor, obs, self.raster)
                sd = SummaryDialog()
                sd.setSummary(self.methodComboBox.currentText(), self.raster, sensor, obs, shooters, time() - start)
                sd.exec_()
        except:
            pass
