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
from PyQt5.QtWidgets import QWidget

FORM_CLASS, _ = uic.loadUiType(
        path.join(path.dirname(__file__), 'sensorWidget.ui')
    )

class SensorWidget(QWidget, FORM_CLASS):
    def __init__(self, parent=None):
        """
        Class constructor.
        :param parent: (QWidget) any widget from Qt5 parent to this dialog.
        """
        super(SensorWidget, self).__init__(parent)
        self.setupUi(self)
