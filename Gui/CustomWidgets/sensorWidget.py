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
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QWidget

from Settings.settings import Settings
from Core.enums import Enums
from Core.Sensor.sensorsManager import SensorsManager
from Core.Sensor.sensor import Sensor
from Gui.CustomWidgets.FeatureForms.featureForm import FeatureForm

FORM_CLASS, _ = uic.loadUiType(
        path.join(path.dirname(__file__), 'sensorWidget.ui')
    )

class SensorWidget(QWidget, FORM_CLASS):
    sensorAdded, sensorEdited = pyqtSignal(Sensor), pyqtSignal(Sensor)
    selectionChanged = pyqtSignal(int)
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
        self.refresh(sensorsList=[])

    def fillSensorComboBox(self, sensorsList):
        """
        Fills all given sensors to the selection combo box.
        :param sensorsList: (list-of-Sensor) sensors to be listed on widget.
        """
        self.sensorComboBox.addItem(self.tr("Select a sensor..."))
        self.sensorComboBox.addItems([])
        # l = [
        #     "{0} (ID = {1})".format(
        #             s['name'] or self.tr("Station {0}").format(s['id'])),
        #             s['id']
        #         ) for s in sensorsList
        # ]

    def clear(self):
        """
        Clears sensor combo box and GUI information, if any.
        """
        self.sensorComboBox.clear()

    def refresh(self, sensorsList):
        """
        Resets widget to initial state.
        :param sensorsList: (list)
        """
        self.clear()
        self.fillSensorComboBox(sensorsList)
        self.setSensorInformation(self.sensor())

    def sensorIdFromIndex(self, idx):
        """
        Gets the sensor ID from item at the given index. If index is invalid None
        is returned.
        :param idx: (int) item index in the sensor selection combo box.
        :return: (int) sensor ID.
        """
        if idx > 0 and self.sensorComboBox.count() > idx:
            # disregard first item ("Select...")
            return int(
                self.sensorComboBox.itemText(idx).split("ID = ")[-1].split(")")[0]
            )
        return None

    def sensorFromIndex(self, idx):
        """
        Gets the sensor from the indicated index. If index is invalid None is returned.
        :param idx: (int) item index in the sensor selection combo box.
        :return: (Sensor) sensor at the indicated index.
        """
        sid = self.sensorIdFromIndex(idx)
        if sid is not None:
            return self._sensorsManager.getSensorFromId(sid)
        return None

    def sensorId(self):
        """
        Gets current sensor ID. Returns None if no selection was made.
        :return: (int) sensor ID.
        """
        if self.sensorComboBox.currentIndex() < 1:
            return None
        # default string for sensor name should have "(ID = $SENSOR_ID)" on it
        return int(self.sensorComboBox.currentText().split("ID = ")[-1].split(")")[0])

    def sensor(self):
        """
        Gets the sensor object for current selection.
        :return: (Sensor) an instance of Sensor object for current selection.
        """
        if self.sensorId() is None:
            return None # should it be a new instance of sensor obj?
        return self._sensorsManager.getSensorFromId(self.sensorId())

    def setSensorInformation(self, sensor):
        """
        Sets sensor information to widget interface.
        :param sensor: (Sensor) sensor to have its info exposed.
        """
        sensor = sensor or self._sensorsManager.newSensor()
        if sensor['status']:
            statusText = '<font color="green">{status}</font>'.format(status=self.tr("active"))
        else:
            statusText = '<font color="red">{status}</font>'.format(status=self.tr("inactive"))
        self.statusLabel.setText(self.tr("Status: {st}").format(st=statusText))
        self.crsLabel.setText(self.tr("CRS: {0}").format(sensor['crs']))
        self.onLabel.setText(sensor['activation_date'])
        self.offLabel.setText(sensor['deactivation_date'] or "-")

    def isEditable(self):
        """
        Verifies whether current selection may be edited.
        :return: (bool) edition status.
        """
        return self.sensorComboBox.currentIndex() < 1

    @pyqtSlot(bool, name="on_sensorComboBox_currentIndexChanged")
    def checkEditButtonStatus(self):
        """
        Updates the edit push button enable status.
        """
        self.updateSensorPushButton.setEnabled(self.isEditable())
        self.setSensorInformation(self.sensor())

    @pyqtSlot(bool, name='on_updateSensorPushButton_clicked')
    def openEditForm(self):
        """
        Opens feature form for current selection in edition mode.
        """
        pass
        
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
