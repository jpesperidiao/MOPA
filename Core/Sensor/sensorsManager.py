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
from Core.Observation.observationsManager import ObservationsManager

class SensorsManager():
    """
    Handles sensor objects. Later on, it should be able to handle signals, to always keep
    sensor's information updated to all executions connected to the database (allowing real-
    time updates to all MOPA users at once.)
    """
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
        param = dict()
        info = self.settings.getSensor(sensorId)
        if info != tuple():
            param['id'], param['name'], param['coordinates'], param ['epsg'], param['activation_date'],\
            param['deactivation_date'], param['status'] = info
            param['coordinates'] = tuple([float(c) for c in param['coordinates'].split(',')])
            param['status'] = bool(param['status'])
            param['id'] = int(param['id'])
            param['epsg'] = int(param['epsg'])
        return Sensor(param)

    def sensorExists(self, sensor):
        """
        Checks if a sensor exists into database.
        :param sensor: (Sensor) sensor instance.
        :return: (bool) if sensor exists into the database.
        """
        return self.idExists(sensor['id'])

    def idExists(self, sensorId):
        """
        Checks if a sensor exists into database from its ID.
        :param sensorId: (int) sensor ID to be checked.
        :return: (bool) if the database has a sensor entry with the given ID.
        """
        return sensorId in self.allSensors()

    def sensorFromAttributes(self, parameters):
        """
        Gets a Sensor instance based on a set of attributes.
        :param paremteres: (dict) attribute set.
        :return: (Sensor) a sensor instance if attribute set is valid, or a blank instance.
        """
        s = Sensor(parameters)
        return s if s.isValid() else self.newSensor()

    def newSensor(self):
        """
        Gets a fresh and empty insance of a sensor.
        :return: (Sensor) new sensor.
        """
        return Sensor({})

    def addSensor(self, coordinates, epsg, name=None, status=True):
        """
        Add a sensor to the database.
        :param coordinates: (tuple-of-floats) tuple with sensor's coordinates.
        :param epsg: (int) CRS authentication ID.
        :param name: (str) station's friendly name.
        :param status: (bool) sensor's activation status.
        :return: (Sensor) sensor object.
        """
        self.settings.addSensor(coordinates, epsg, name, status)

    def rasterHasSensor(self, raster, sensor):
        """
        Checks if a sensor is inside a given raster.
        :param raster: (RasterLayer) target raster.
        :param sensor: (Sensor) sensor to be checked.
        :return: (bool) whether sensor is inside raster bounding box.
        """
        return raster.hasPoint(sensor['coordinates'])

    def allSensors(self):
        """
        Get all available sensors from database.
        :return: (dict-of-Sensors) all sensors mapped by sensor ID.
        """
        sensors = dict()
        for item in self.settings.sensorsItems():
            param = dict()
            param['id'], param['name'], param['coordinates'], param ['epsg'], param['activation_date'],\
            param['deactivation_date'], param['status'] = item
            param['coordinates'] = tuple([float(c) for c in param['coordinates'].split(',')])
            param['status'] = bool(param['status'])
            param['id'] = int(param['id'])
            param['epsg'] = int(param['epsg'])
            sensors[param['id']] = Sensor(param)
        return sensors

    def availableSensors(self):
        """
        Get all available sensors from database.
        :return: (dict-of-Sensors) all sensors mapped by sensor ID.
        """
        sensors = dict()
        for item in self.settings.sensorsItems():
            param = dict()
            param['id'], param['name'], param['coordinates'], param ['epsg'], param['activation_date'],\
            param['deactivation_date'], param['status'] = item
            param['coordinates'] = tuple([float(c) for c in param['coordinates'].split(',')])
            param['status'] = bool(param['status'])
            param['id'] = int(param['id'])
            param['epsg'] = int(param['epsg'])
            if param['status']:
                sensors[param['id']] = Sensor(param)
        return sensors

    def getSensorsInsideRaster(self, raster):
        """
        Gets all available sensors inside raster area that share the same CRS.
        :param raster: (RasterLayer) raster to be checked for sensors.
        :return: (list-of-Sensors) all available sensors inside of a given raster.
        """
        if not raster.isValid():
            return []
        sensors = dict()
        epsg = raster.epsg()
        for item in self.settings.sensorsItems():
            param = dict()
            param['id'], param['name'], param['coordinates'], param ['epsg'], param['activation_date'],\
            param['deactivation_date'], param['status'] = item
            param['coordinates'] = tuple([float(c) for c in param['coordinates'].split(',')])
            param['status'] = bool(param['status'])
            param['id'] = int(param['id'])
            param['epsg'] = int(param['epsg'])
            if param ['epsg'] != epsg:
                # for now, just ignore, later reprojection should be applied
                continue
            elif raster.hasPoint(param['coordinates']):
                sensors[param['id']] = Sensor(param)
        return sensors

    def removeSensor(self, sensor):
        """
        Removes sensor from database.
        :param sensor: (Sensor) sensor to be removed from database.
        """
        # TODO
        pass

    def updateSensor(self, sensor):
        """
        Updates the attribute values for a given sensor into the database.
        :param sensor: (Sensor) sensor to be updated on the database.
        """
        # TODO
        pass

    def getObservationsFromSensor(self, sensorId):
        """
        Gets all observations from a given sensor.
        :param sensorId: (int) sensor ID.
        :return: (list-of-Observation) observations made from a given sensor.
        """
        return ObservationsManager().getObservationsFromSensor(sensorId)
        