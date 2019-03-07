# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MOPA
                                 An independet project
 Método de Obtenção da Posição de Atirador
                              -------------------
        begin                : 2018-03-06
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

from os import path
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget

from Settings.settings import Settings
from Core.enums import Enums
from Core.Sensor.sensorsManager import SensorsManager
from Gui.CustomWidgets.FeatureForms.featureForm import FeatureForm

FORM_CLASS, _ = uic.loadUiType(
        path.join(path.dirname(__file__), 'sensorWidget.ui')
    )

class SensorWidget(QWidget, FORM_CLASS):
    def __init__(self, settings=None, parent=None):
        """
        Class constructor.
        :param parent: (QWidget) any widget from Qt5 parent to this dialog.
        """
        super(SensorWidget, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.settings = settings if settings is not None else Settings()
        self._sensorsManager = SensorsManager(settings)

    def sensor(self):
        """
        Gets the sensor object for current selection.
        :return: (Sensor) an instance of Sensor object for current selection.
        """
        if self.sensorComboBox.currentIndex() < 1:
            return None # should it be a new instance of sensor obj?
        sid = int(self.sensorComboBox.currentText().split("ID = ")[-1].split(")")[0])
        return self._sensorsManager.getSensorFromId(sid)

    def checkEditingMode(self):
        """
        Verifies whether current selection may be edited.
        """
        self.updateSensorPushButton.setEnabled(
            self.sensorComboBox.currentIndex() < 1
        )

    @pyqtSlot(bool, name='on_updateSensorPushButton_clicked')
    def openEditForm(self):
        """
        Opens feature form for current selection in edition mode.
        """
        
    @pyqtSlot(bool, name='on_addSensorPushButton_clicked')
    def openForm(self, isEditable=True):
        """
        Opens attribute form for a given observation. Updates observation if necessary.
        :param sensor: (Observation) the observation to have its attributes exposed.
        :param isEditable: (bool) indicates whether attributes may be updated.
        """
        form = FeatureForm(self._sensorsManager.newSensor(), isEditable, self.parent)
        # form.setTitle(form.tr("Observation Attributes Form - add new sensor"))
        if form.exec_() == Enums.Finished:
            attributes = form.read()
            self._sensorsManager.addSensor(
                attributes['coordinates'],
                attributes['epsg'],
                attributes['name'],
                attributes['status']
            )