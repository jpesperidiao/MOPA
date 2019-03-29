#!./.dev/venv/bin python3
# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MOPA
                     An independet project
 Método de Obtenção da Posição de Atirador
                  -------------------
     begin                : 2019-01-15
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

import locale
from os import path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QSettings, qVersion, QCoreApplication, QTranslator

from Settings.settings import Settings
from Gui.CustomWidgets.mainWindow import MainWindow

# attach remote debugger only if available
try:
    import ptvsd
    ptvsd.enable_attach(address=('localhost', 9875))
except:
    pass

# provide internationalization
locale_ = locale.getdefaultlocale()[0][0:2]
locale_path = path.join(
            path.dirname(__file__),
            'i18n',
            'mopa_{}.qm'.format(locale_)
        )
if path.exists(locale_path):
    translator = QTranslator()
    translator.load(locale_path)
    if qVersion() > '4.3.3':
        QCoreApplication.installTranslator(translator)

app = MainWindow()
app.show()
QApplication.instance().exec_()
