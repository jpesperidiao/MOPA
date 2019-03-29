# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MOPA
                                 An independet project
 Método de Obtenção da Posição de Atirador
                              -------------------
        begin                : 2019-03-06
        git sha              : $Format:%H$
        copyright            : (C) 2019 by João P. Esperidião
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

from Core.enums import Enums
from Settings.settings import Settings
from Core.Observation.observation import Observation
from Core.Observation.observationsManager import ObservationsManager
from Gui.CustomWidgets.FeatureForms.featureForm import FeatureForm

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
        :param idx: (int) item index in the observation selection combo box.
        :return: (int) observation ID.
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
        oid = self.obsIdFromIndex(idx)
        if oid is not None:
            return self._obsManager.observationFromId(oid)
        return None

    def obsId(self):
        """
        Gets current observation's ID. Returns None if no selection was made.
        :return: (int) observation's ID.
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
            attributes['azimuth'] = float(attributes['azimuth'])
        except:
            pass
        try:
            attributes['zenith'] = float(attributes['zenith'])
        except:
            pass
        try:
            attributes['sensorId'] = int(attributes['sensorId'])
        except:
            pass
        if not isinstance(attributes['date'], str):
            try:
                attributes['date'] = str(attributes['date'])
            except:
                pass
        return attributes

    def checkFormValidity(self, form, checkIfExists=False):
        """
        Checks form validity.
        :param form: (FeatureForm) form to have its contents checked.
        :param checkIfExists: (bool) indicates whether entry existance should be checked.
        :return: (bool) form validity status.
        """
        attr = self.parametersFromForm(form.read())
        ir = self._obsManager.newObservation().invalidationReason(attr)
        if checkIfExists and self._obsManager.idExists(attr['id']):
            ir = self.tr("Observation ID {0} already exists into the database.").\
                format(attr['id'])
        form.setInvalidationMessage(ir)
        return ir == ''

    @pyqtSlot(bool, name='on_updateObservationPushButton_clicked')
    def openEditForm(self):
        """
        Opens feature form for current selection in edition mode.
        """
        form = FeatureForm(self.currentObservation(), True, self.parent)
        form.setWindowTitle(form.tr("Edit observation's attributes"))
        form.fieldReadOnly('id', True) # since it is an EDITION, id should be kept the same.
        form.okButtonClicked.connect(self.checkFormValidity)
        if form.exec_() == Enums.Finished:
            attr = self.parametersFromForm(form.read())
            obs = self._obsManager.observationFromAttributes(attr)
            if obs.isValid():
                self._obsManager.updateObservation(obs)
                self.obsComboBox.setItemText(
                    self.obsComboBox.currentIndex(),
                    self.tr("Observation {0}").format(obs['id'])
                )
                # and update its attributes to GUI
                self.setObsInformation(obs)
                form.blockSignals(True)
                del form
                self.observationEdited.emit(obs)

    @pyqtSlot(bool, name='on_addObservationPushButton_clicked')
    def openForm(self):
        """
        Opens attribute form to be filled in order to add a new sensor.
        """
        form = FeatureForm(self._obsManager.newObservation(), True, self.parent)
        form.setWindowTitle(self.tr("Add a new observation"))
        form.okButtonClicked.connect(lambda f : self.checkFormValidity(f, True))
        if form.exec_() == Enums.Finished:
            attr = self.parametersFromForm(form.read())
            obs = self._obsManager.observationFromAttributes(attr)
            if obs.isValid():
                self._obsManager.addObservation(
                    azimuth=obs['azimuth'], zenith=obs['zenith'],\
                    sensorId=obs['sensorId']
                )
                form.blockSignals(True)
                del form
                name = self.tr("Observation {0}").format(obs['id'])
                self.obsComboBox.addItem(name)
                self.observationAdded.emit(obs)
