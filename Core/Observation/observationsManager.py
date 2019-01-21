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
from .observation import Observation

class ObservationsManager():
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

    def getObservationsFromSensor(self, sensorId):
        """
        Gets a observation from database using its
        :param sensorId: (int) target sensor ID.
        :return: (Observation) observation object.
        """
        observations = dict()
        for info in self.settings.observationsItems():
            param = dict()
            param['id'], param['azimuth'], param ['zenith'], param['sensorId'],\
            param['date'] = info
            param['azimuth'] = float(param['azimuth'])
            param['zenith'] = float(param['zenith'])
            param['id'] = int(param['id'])
            param['sensorId'] = int(param['sensorId'])
            if param['sensorId'] == sensorId:
                observations[param['id']] = Observation(param)
        return observations

    def getNewObservation(self):
        """
        Gets a fresh and empty insance of a observation.
        :return: (Observation) new observation.
        """
        return Observation({})

    def addObservation(self, azimuth, zenith, sensorId):
        """
        Add a observation to the database.
        :param azimuth: (float) tuple with observation's coordinates.
        :param zenith: (float) CRS authentication ID.
        :param sensorId: (int) observation's activation status.
        """
        self.settings.addObservation(azimuth, zenith, sensorId)

    def allObservations(self):
        """
        Get all available observations from database.
        :return: (dict-of-Observations) all observations mapped by observation ID.
        """
        observations = dict()
        for item in self.settings.observationsItems():
            param = dict()
            param['id'], param['azimuth'], param ['zenith'], param['sensorId'],\
            param['date'] = item
            param['azimuth'] = float(param['azimuth'])
            param['zenith'] = float(param['zenith'])
            param['id'] = int(param['id'])
            param['sensorId'] = int(param['sensorId'])
            observations[param['id']] = Observation(param)
        return observations

    def removeObservation(self, observation):
        """
        Removes observation from database.
        :param observation: (Sensor) observation to be removed from database.
        """
        # TODO
        pass
