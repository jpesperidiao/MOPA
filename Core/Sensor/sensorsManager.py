# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MOPA
                                 An independet project
 Método de Obtenção da Posição de Atirador
                              -------------------
        begin                : 2018-01-13
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

from Settings.settings import Settings
from .sensor import Sensor

class SensorsManager():
    def __init__(self, settings=None):
        """
        Class constructor.
        :param settings: (Settings) MOPA's settings object.
        """
        if settings is None:
            # the option of a settings rather than a new instance of Settings is given
            # in order to allow custom settings later on. 
            settings = Settings()
        self.settings = settings

    def getSensorFromId(self, sensorId):
        """
        Gets a sensor from database using its
        :param sensorId: (int) sensor ID.
        :return: (Sensor) sensor object.
        """
        self.settings.getSensor(sensorId)

    def addSensor(self, coordinates, epsg, status=True):
        """
        Add a sensor to the database.
        :param coordinates: (tuple-of-floats) tuple with sensor's coordinates.
        :param epsg: (int) CRS authentication ID.
        :param status: (bool) sensor's activation status.
        :return: (Sensor) sensor object.
        """
        self.settings.addSensor(coordinates, epsg, status)

    def rasterHasSensor(self, raster, sensor):
        """
        Checks if a sensor is inside a given raster.
        :param raster: (RasterLayer) target raster.
        :param sensor: (Sensor) sensor to be checked.
        :return: (bool) whether sensor is inside raster bounding box.
        """
        return raster.hasPoint(sensor['coordinates'])

    def availableSensors(self):
        """
        Get all available sensors from database.
        :return: (list-of-Sensors) all sensors.
        """
        sensors = []
        for item in self.settings.sensorsItems():
            param = dict()
            param['id'], param['coordinates'], param ['epsg'], param['activation_date'],\
            param['deactivation_date'], param['status'] = item
            sensors.append(Sensor(param))
        return sensors

    def getSensorsInsideRaster(self, raster):
        """
        Gets all available sensors inside raster area that share the same CRS.
        :param raster: (RasterLayer) raster to be checked for sensors.
        :return: (list-of-Sensors) all available sensors inside of a given raster.
        """
        if not raster.isValid():
            return []
        sensors = []
        epsg = raster.epsg()
        for sensor in self.availableSensors():
            if sensor['epsg'] != epsg:
                continue
            elif raster.hasPoint(sensor['coordinates']):
                sensors.append(sensor)
        return sensors
