# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MOPA
            An independet project
 Método de Obtenção da Posição de Atirador
            -------------------
     begin       : 2018-03-06
     git sha     : $Format:%H$
     copyright      : (C) 2018 by João P. Esperidião
     email       : joao.p2709@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.              *
 *                         *
 ***************************************************************************/
"""

from time import sleep
from os import path
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QMessageBox

from Core.enums import Enums
from Core.Sensor.sensorsManager import SensorsManager

FORM_CLASS, _ = uic.loadUiType(path.join(path.dirname(__file__), "featureForm.ui"))

class FeatureForm(QDialog, FORM_CLASS):
    """
    Class desgined to be used as base for every feature attribute exposure,
    edition or read-only forms.
    """
    editingModeChanged = pyqtSignal(bool)
    okButtonClicked = pyqtSignal(QDialog)
    def __init__(self, feature, isEditable=True, parent=None):
        """
        Class constructor.
        :param feature: (Sensor/Observation) feature to have its 
        :param parent: (QWidget) widget to wich this item is related to.
        """
        super(FeatureForm, self).__init__(parent)
        self.setupUi(self)
        self.feature = feature
        self.isEditable = isEditable
        self.parent = parent
        self._invalidationReason = ""
        self.widgets = self.setupAttributes()

    def clearWidgets(self):
        """
        Clears all attributes' widgets added to the form.
        """
        for wMap in self.widgets.values():
            for w in wMap.values():
                w.setParent(None)
                del w

    def setupAttributes(self):
        """
        Adds all labels and lines for displaying/editing attributes.
        :return: (dict) a map with all generated widgets for each attribute.
        """
        widgets = dict()
        for row, attr in enumerate(self.feature.attributes()):
            if attr not in widgets:
                widgets[attr] = dict()
                widgets[attr]["label"] = QLabel(attr)
                widgets[attr]["lineEdit"] = QLineEdit()
                widgets[attr]["lineEdit"].setText(
                        '' if self.feature[attr] is None \
                            else self.feature[attr] if isinstance(self.feature[attr], str) \
                            else str(self.feature[attr])
                    )
                widgets[attr]["lineEdit"].setReadOnly(not self.isEditable)
                self.attributesGridLayout.addWidget(widgets[attr]["label"], row, 0)
                self.attributesGridLayout.addWidget(widgets[attr]["lineEdit"], row, 1)
        return widgets

    def setEditable(self, active):
        """
        Sets if feature is to be editable or not.
        :param active: (bool) whether feature is editable.
        """
        self.isEditable = active
        self.editingModeChanged.emit(active)

    def setInvalidationMessage(self, msg):
        """
        Changes the value of invalidation message for the form. If any, it will
        make the form invalid.
        :param msg: (msg) invalidation message.
        """
        self._invalidationReason = msg

    def invalidationMessage(self):
        """
        Gets current invalidation reason from form.
        :return: (str) invalidation message.
        """
        return self._invalidationReason

    def read(self):
        """
        Reads form's contents and return as a map to attributes.
        :return: (dict) all attributes read from form (which will come as strings!).
        """
        attributes = dict()
        for attr, wMap in self.widgets.items():
            attributes[attr] = wMap["lineEdit"].text()
        return attributes

    def updateForm(self):
        """
        Updates all attributes from feature.
        """
        for attr, wMap in self.widgets.items():
            wMap['lineEdit'].setText(self.feature[attr])
            wMap["lineEdit"].setReadOnly(not self.isEditable)

    def fieldReadOnly(self, field, readOnly):
        """
        Sets read only status to a field entry on the form, if it exists.
        :param field: (str) field name.
        :param readOnly: (bool) whether attribute should be can (not) be edited.
        :return: (bool) read only status. If field doesn't exist, False will be returned.
        """
        if field in self.widgets:
            self.widgets[field]['lineEdit'].setReadOnly(readOnly)
            return readOnly
        return False

    def updateAttribute(self, attribute, value):
        """
        Updates attribute value to be exhibited on the form.
        :param attribute: (str) attribute name to be updated.
        :param value: (str/int/float) new attribute value to be displayed.
        :return: (bool) whether method was effective (e.g. updated the displayed value)
        """
        if self.isEditable and attribute in self.widgets:
            self.widgets[attribute]['lineEdit'].setText(value)
            return True
        return False

    @pyqtSlot(bool, name="on_okPushButton_clicked")
    @pyqtSlot(bool, name="on_cancelPushButton_clicked")
    def finish(self):
        """
        Closes the form and emit the proper execution code.
        """
        code = {
            self.tr('Ok') : Enums.Finished,
            self.tr('Cancel') : Enums.Cancelled,
        }[self.sender().text()]
        if code == Enums.OkButton:
            self.okButtonClicked.emit(self)
        sleep(.1)
        if code == Enums.Finished and self.invalidationMessage() != '':
            mb = QMessageBox(self)
            QMessageBox.warning(self, self.tr("Invalid attribute!"), self.invalidationMessage())
        else:
            self.done(code)

    def keyPressEvent(self, e):
        """
        Method called whenever a key is pressed.
        :param: (KeyboardPressEvent)
        """
        codeList = {
            Qt.Key_Return : Enums.Finished,
            Qt.Key_Escape : Enums.Cancelled
        }
        if e.key() in codeList:
            self.done(codeList[e.key()])