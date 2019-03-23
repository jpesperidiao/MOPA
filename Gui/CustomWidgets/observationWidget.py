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
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget

from Settings.settings import Settings
from Core.Observation.observation import Observation
from Core.Observation.observationsManager import ObservationsManager

FORM_CLASS, _ = uic.loadUiType(
        path.join(path.dirname(__file__), 'observationWidget.ui')
)

class ObservationWidget(QWidget, FORM_CLASS):
    observationAdded, observationEdited = pyqtSignal(Observation), pyqtSignal(Observation)
    selectionChanged = pyqtSignal(int)
    def __init__(self, parent=None, settings=None):
        """
        Class constructor.
        :param parent: (QWidget) any widget from Qt5 parent to this dialog.
        :param settings: (Settings) MOPA's settings database manager.
        """
        super(ObservationWidget, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.settings = settings if settings is not None else Settings()
        self._obsManager = ObservationsManager(self.settings)
        self.refresh(obsList=[])

    def clear(self):
        """
        Clears observation combo box and GUI information, if any.
        """
        self.obsComboBox.clear()

    def fillObsComboBox(self, obsList):
        """
        Fills all given observations to the selection combo box.
        :param obsList: (list-of-Observation) observations to be listed on widget.
        """
        self.clear()
        self.obsComboBox.addItem(self.tr("Select an observation..."))
        self.obsComboBox.addItems([
            "Observation {0}".format(o['id']) for o in obsList
        ])

    def refresh(self, obsList):
        """
        Resets widget to initial state.
        :param obsList: (list-of-Observation) observations to be listed on widget.
        """
        self.clear()
        self.fillObsComboBox(obsList)
        self.setObsInformation(self.currentObservation())

    def obsIdFromIndex(self, idx):
        """
        Gets the observation ID from item at the given index. If index is invalid None
        is returned.
        :param idx: (int) item index in the sensor selection combo box.
        :return: (int) sensor ID.
        """
        if idx > 0 and self.obsComboBox.count() > idx:
            return int(self.obsComboBox.itemText(idx).split(" ")[-1])
        return None

    def observationFromIndex(self, idx):
        """
        Gets the observation from the indicated index. If index is invalid None is returned.
        :param idx: (int) item index in the observation selection combo box.
        :return: (Observation) observation instance from the indicated index.
        """
        sid = self.sensorIdFromIndex(idx)
        if sid is not None:
            return self._obsManager.observationFromId(sid)
        return None

    def obsId(self):
        """
        Gets current sensor ID. Returns None if no selection was made.
        :return: (int) sensor ID.
        """
        if self.obsComboBox.currentIndex() < 1:
            return None
        return int(self.obsComboBox.currentText().split(" ")[-1])

    def currentObservation(self):
        """
        Gets the observation object for current selection.
        :return: (Observation) an instance of Observation object for current selection.
        """
        if self.obsId() is None:
            return None # should it be a new instance of observation obj?
        return self._obsManager.observationFromId(self.obsId())

    def setObsInformation(self, obs):
        """
        Sets observation information to widget interface.
        :param obs: (Observation) observation to have its info exposed.
        """
        obs = obs or self._obsManager.newObservation()
        self.azLabel.setText(self.tr("Azimuth: {0:.2f}").format(obs['azimuth']))
        self.zenLabel.setText(self.tr("Vertical angle: {0:.2f}").format(obs['zenith']))
        self.dateLabel.setText(self.tr("Observation date: {0}").format(obs['date']))
        title = self.tr("Event information")
        if obs.isValid():
            title += self.tr(" from station ID = {0}").format(obs['sensorId'])
        self.groupBox.setTitle(title)

    def isEditable(self):
        """
        Verifies whether current selection may be edited.
        :return: (bool) edition status.
        """
        return not self.obsComboBox.currentIndex() < 1

    @pyqtSlot(int, name="on_obsComboBox_currentIndexChanged")
    def checkEditButtonStatus(self, idx):
        """
        Updates the edit push button enable status.
        :param idx: (int) current index.
        """
        self.updateObservationPushButton.setEnabled(self.isEditable())
        self.setObsInformation(self.currentObservation())
        self.selectionChanged.emit(idx)

    # def parametersFromForm(self, attributes):
    #     """
    #     Sets the correct variable types from form info.
    #     :param attributes: (dict) form's info.
    #     :return: (dict) values reasigned to its correct variable type. 
    #     """
    #     try:
    #         attributes['id'] = int(attributes['id'])
    #     except:
    #         pass
    #     try:
    #         attributes['epsg'] = int(attributes['epsg'])
    #     except:
    #         pass
    #     try:
    #         attributes['coordinates'] = tuple([
    #                 float(n) for n in attributes['coordinates'][1:-1].split(', ')
    #             ])
    #     except:
    #         pass
    #     if attributes['status'].lower() in ("true", "false"):
    #         attributes['status'] = attributes['status'].lower() == "true"
    #     return attributes

    # def checkFormValidity(self, form, checkIfExists=False):
    #     """
    #     Checks form validity.
    #     :param form: (FeatureForm) form to have its contents checked.
    #     :param checkIfExists: (bool) indicates whether entry existance should be checked.
    #     :return: (bool) form validity status.
    #     """
    #     attr = self.parametersFromForm(form.read())
    #     ir = self._obsManager.newSensor().invalidationReason(attr)
    #     if ir == '' and attr['epsg'] == 0:
    #         ir = self.tr("Invalid CRS.")
    #     if checkIfExists and self._obsManager.idExists(attr['id']):
    #         ir = self.tr("Sensor ID {0} already exists into the database.").\
    #             format(attr['id'])
    #     form.setInvalidationMessage(ir)
    #     return ir == ''

    # @pyqtSlot(bool, name='on_updateSensorPushButton_clicked')
    # def openEditForm(self):
    #     """
    #     Opens feature form for current selection in edition mode.
    #     """
    #     form = FeatureForm(self.currentSensor(), True, self.parent)
    #     # form.setTitle(form.tr("Observation Attributes Form - add new sensor"))
    #     form.okButtonClicked.connect(self.checkFormValidity)
    #     if form.exec_() == Enums.Finished:
    #         attr = self.parametersFromForm(form.read())
    #         sensor = self._obsManager.sensorFromAttributes(attr)
    #         if sensor.isValid():
    #             self._obsManager.updateSensor(sensor)
    #             form.blockSignals(True)
    #             del form
    #             self.sensorEdited.emit(sensor)

    # @pyqtSlot(bool, name='on_addSensorPushButton_clicked')
    # def openForm(self):
    #     """
    #     Opens attribute form to be filled in order to add a new sensor.
    #     """
    #     form = FeatureForm(self._obsManager.newSensor(), True, self.parent)
    #     # form.setTitle(form.tr("Observation Attributes Form - add new sensor"))
    #     form.okButtonClicked.connect(lambda f : self.checkFormValidity(f, True))
    #     if form.exec_() == Enums.Finished:
    #         attr = self.parametersFromForm(form.read())
    #         sensor = self._obsManager.sensorFromAttributes(attr)
    #         if sensor.isValid():
    #             self._obsManager.addSensor(
    #                 sensor['coordinates'],
    #                 sensor['epsg'],
    #                 sensor['name'],
    #                 sensor['status']
    #             )
    #             form.blockSignals(True)
    #             del form
    #             name = "{0} (ID = {1})".format(
    #                 sensor['name'] or self.tr("Station {0}").format(sensor['id']), sensor['id']
    #             )
    #             self.obsComboBox.addItem(name)
    #             self.sensorAdded.emit(sensor)
