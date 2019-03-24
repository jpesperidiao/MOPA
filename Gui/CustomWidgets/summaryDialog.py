# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MOPA
                                 An independet project
 Método de Obtenção da Posição de Atirador
                              -------------------
        begin                : 2019-02-02
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
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QFileDialog

FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'summaryDialog.ui'))

class SummaryDialog(QDialog, FORM_CLASS):
    def __init__(self, html=None, parent=None):
        """
        Class constructor.
        :param parent: (QWidget) any widget from Qt5 parent to this dialog.
        """
        super(SummaryDialog, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.setHtml(html)

    def setHtml(self, html):
        """
        Sets HTML text to GUI.
        :param html: (str) html text to be added.
        """
        html = "" if html is None else html
        self.summaryTextBrowser.setHtml(html)

    def addToHtml(self, textToAdd):
        """
        Appends text to existing one.
        :param textToAdd: (str) text to be added to GUI.
        """
        html = self.summaryTextBrowser.toHtml()
        self.summaryTextBrowser.setHtml(html + textToAdd)

    def clearHtml(self):
        """
        Clears text from GUI.
        """
        self.summaryTextBrowser.setHtml("")

    def template(self):
        """
        Gets summary template contents.
        :return: (str) template's contents.
        """
        with open(os.path.join(os.path.dirname(__file__), 'summaryTemplate.html'), 'r') as f:
            return f.read()

    def setSummary(self, method, dem, sensor, obs, shooters, elapsedTime):
        """
        Sets summary to interface.
        :param method: (str) name of method used to finding the shooter.
        :param dem: (RasterLayer) DEM used.
        :param sensor: (Sensor) sensor used for shooter detection.
        :param obs: (Observation) observation detected by sensor.
        :param shooters: (set) shooters found.
        :param method: (str) method used for finding the shooter.
        :param elapsedTime: (float) elapsed time in seconds.
        """
        template = self.template()
        xMin, xMax, yMin, yMax = dem.extents()
        sensorY, sensorX, sensorZ = sensor['coordinates']
        template = template.replace('SENSOR_Y', "{0}".format(sensorY))\
                    .replace('SENSOR_X', "{0}".format(sensorX))\
                    .replace('SENSOR_Z', "{0:.2f}".format(sensorZ))\
                    .replace('SENSOR_EPSG', "{0}".format(sensor['epsg']))\
                    .replace('AZIMUTH', "{0:.3f}".format(obs['azimuth']))\
                    .replace('ZENITH', "{0:.3f}".format(obs['zenith']))\
                    .replace('METHOD_NAME', method)\
                    .replace('EXEC_TIME', "{0:.3f} s".format(elapsedTime))\
                    .replace('RASTER_FILEPATH', dem.directory)\
                    .replace('RASTER_UNITS', self.tr('degrees') if dem.isGeographic() else self.tr('meters'))\
                    .replace('RASTER_CRS', dem.projection())\
                    .replace('SPATIAL_RESOLUTION', "{0:.2f} m".format(dem.spatialResolution()))\
                    .replace('ROW_COUNT', str(dem.width()))\
                    .replace('COL_COUNT', str(dem.height()))\
                    .replace('Y_AXIS', self.tr('Latitude') if dem.isGeographic() else self.tr('Northing'))\
                    .replace('X_AXIS', self.tr('Longitude') if dem.isGeographic() else self.tr('Easting'))\
                    .replace('Z_AXIS', self.tr('Altitude'))\
                    .replace('MIN_Y', str(yMin))\
                    .replace('MIN_X', str(xMin))\
                    .replace('MIN_Z', "{0:.2f}".format(dem.min()))\
                    .replace('MAX_Y', str(yMax))\
                    .replace('MAX_X', str(xMax))\
                    .replace('MAX_Z', "{0:.2f}".format(dem.max()))
        shootersString = ""
        for idx, shooter in enumerate(shooters):
            row, col, h = shooter
            y, x = dem.pixelToCoordinates(col, row)
            shootersString += """
            <tr>
                <td style="text-align: center; width: 110%;"><strong>SH_NUMBER</strong></td>
                <td style="text-align: center; width: 110%;">SH_COL</td>
                <td style="text-align: center; width: 110%;">SH_ROW</td>
                <td style="text-align: center; width: 110%;">SH_Y</td>
                <td style="text-align: center; width: 110%;">SH_X</td>
                <td style="text-align: center; width: 110%;">SH_HEIGHT</td>
            </tr>
            """.replace('SH_NUMBER', str(idx + 1))\
                .replace('SH_COL', str(col))\
                .replace('SH_ROW', str(row))\
                .replace('SH_Y', str(y))\
                .replace('SH_X', str(x))\
                .replace('SH_HEIGHT', "{0:.2f}".format(h))
        self.summaryTextBrowser.setHtml(template.replace('SHOOTERS_TABLE', shootersString))

    @pyqtSlot(bool, name='on_savePushButton_clicked')
    def saveHtml(self):
        """
        Exports text.
        :return: (str) output path.
        """
        html = self.summaryTextBrowser.toHtml()
        fd = QFileDialog()
        filename = fd.getSaveFileName(caption=self.tr('Select a Path to Log'),filter=self.tr('HTML Files (*.html)'))
        filename = filename[0] if isinstance(filename, tuple) else filename
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html)
        return filename

    @pyqtSlot(bool, name='on_closePushButton_clicked')
    def exit(self):
        """
        Closes dialog.
        """
        self.close()
