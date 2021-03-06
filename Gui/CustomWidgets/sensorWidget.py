# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MOPA
                                 An independet project
 Método de Obtenção da Posição de Atirador
                              -------------------
        begin                : 2019-03-06
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
from Core.ProcessingTools.geoprocessingTools import GeoprocessingTools
from Core.Sensor.sensorsManager import SensorsManager
from Core.Sensor.sensor import Sensor
from Gui.CustomWidgets.FeatureForms.featureForm import FeatureForm

FORM_CLASS, _ = uic.loadUiType(
        path.join(path.dirname(__file__), 'sensorWidget.ui')
    )

class SensorWidget(QWidget, FORM_CLASS):
    sensorAdded, sensorEdited = pyqtSignal(Sensor), pyqtSignal(Sensor)
    selectionChanged = pyqtSignal(int)
    def __init__(self, parent=None, settings=None):
        """
        Class constructor.
        :param parent: (QWidget) any widget from Qt5 parent to this dialog.
        :param settings: (Settings) MOPA's settings database manager.
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
        self.sensorComboBox.addItems([
            "{0} (ID = {1})".format(
                    s['name'] or self.tr("Station {0}").format(s['id']), s['id']
                ) for s in sensorsList
        ])

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
        self.setSensorInformation(self.currentSensor())

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

    def currentSensor(self):
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
        self.crsLabel.setText(self.tr("CRS: {0}").format(
                                    GeoprocessingTools.projectionFromEpsg(sensor['epsg']) or '-'
                                )
                            )
        onDate = self.tr("Activation date: {0}").format(sensor['activation_date'] or "-")
        self.onLabel.setText(onDate)
        offDate = self.tr("Deactivation date: {0}").format(sensor['deactivation_date'] or "-")
        self.offLabel.setText(offDate)
        x, y, z = sensor['coordinates'] if sensor.isValid() else ('-', '-', '-')
        if sensor['epsg'] and GeoprocessingTools.isGeographic(sensor['epsg']):
            axisX, axisY = self.tr("Longitude"), self.tr("Latitude")
        else:
            axisX, axisY = self.tr("Easting"), self.tr("Northing")
        self.xLabel.setText(self.tr("{0}: {1}").format(axisX, x))
        self.yLabel.setText(self.tr("{0}: {1}").format(axisY, y))
        self.zLabel.setText(self.tr("Altitude: {0} m").format(z))

    def isEditable(self):
        """
        Verifies whether current selection may be edited.
        :return: (bool) edition status.
        """
        return not self.sensorComboBox.currentIndex() < 1

    @pyqtSlot(int, name="on_sensorComboBox_currentIndexChanged")
    def checkEditButtonStatus(self, idx):
        """
        Updates the edit push button enable status.
        :param idx: (int) current index.
        """
        self.updateSensorPushButton.setEnabled(self.isEditable())
        self.setSensorInformation(self.currentSensor())
        self.selectionChanged.emit(idx)

    def parametersFromForm(self, attributes):
        """
        Sets the correct variable types from form info.
        :param attributes: (dict) form's info.
        :return: (dict) values reasigned to its correct variable type. 
        """
        try:
            attributes['id'] = int(attributes['id'])
        except:
            pass
        try:
            attributes['epsg'] = int(attributes['epsg'])
        except:
            pass
        try:
            attributes['coordinates'] = tuple([
                    float(n) for n in attributes['coordinates'][1:-1].split(', ')
                ])
        except:
            pass
        attributes['status'] = attributes['status'].lower().strip() == "true" and \
                                attributes['deactivation_date'] == ""
        return attributes

    def checkFormValidity(self, form, checkIfExists=False):
        """
        Checks form validity.
        :param form: (FeatureForm) form to have its contents checked.
        :param checkIfExists: (bool) indicates whether entry existance should be checked.
        :return: (bool) form validity status.
        """
        attr = self.parametersFromForm(form.read())
        ir = self._sensorsManager.newSensor().invalidationReason(attr)
        if ir == '' and attr['epsg'] == 0:
            ir = self.tr("Invalid CRS.")
        if checkIfExists and self._sensorsManager.idExists(attr['id']):
            ir = self.tr("Sensor ID {0} already exists into the database.").\
                format(attr['id'])
        form.setInvalidationMessage(ir)
        return ir == ''

    @pyqtSlot(bool, name='on_updateSensorPushButton_clicked')
    def openEditForm(self):
        """
        Opens feature form for current selection in edition mode.
        """
        form = FeatureForm(self.currentSensor(), True, self.parent)
        form.setWindowTitle(self.tr("Edit sensor ID = {0}".format(self.sensorId())))
        form.fieldReadOnly('id', True) # since it is an EDITION, id should be kept the same.
        form.okButtonClicked.connect(self.checkFormValidity)
        if form.exec_() == Enums.Finished:
            attr = self.parametersFromForm(form.read())
            sensor = self._sensorsManager.sensorFromAttributes(attr)
            if sensor.isValid():
                self._sensorsManager.updateSensor(sensor)
                # once sensor was confirmed as updated, current name could've changed
                self.sensorComboBox.setItemText(
                    self.sensorComboBox.currentIndex(),
                    "{0} (ID = {1})".format(
                        sensor['name'] or self.tr("Station {0}").format(sensor['id']),
                        sensor['id']
                        )
                )
                # and update its attributes to GUI
                self.setSensorInformation(sensor)
                form.blockSignals(True)
                del form
                self.sensorEdited.emit(sensor)

    @pyqtSlot(bool, name='on_addSensorPushButton_clicked')
    def openForm(self):
        """
        Opens attribute form to be filled in order to add a new sensor.
        """
        form = FeatureForm(self._sensorsManager.newSensor(), True, self.parent)
        form.setWindowTitle(self.tr("Add a new sensor"))
        form.okButtonClicked.connect(lambda f : self.checkFormValidity(f, True))
        if form.exec_() == Enums.Finished:
            attr = self.parametersFromForm(form.read())
            sensor = self._sensorsManager.sensorFromAttributes(attr)
            if sensor.isValid():
                self._sensorsManager.addSensor(
                    sensor['coordinates'],
                    sensor['epsg'],
                    sensor['name'],
                    sensor['status']
                )
                form.blockSignals(True)
                del form
                # name = "{0} (ID = {1})".format(
                #     sensor['name'] or self.tr("Station {0}").format(sensor['id']), sensor['id']
                # )
                # self.sensorComboBox.addItem(name)
                self.sensorAdded.emit(sensor)
