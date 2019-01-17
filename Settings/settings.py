# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MOPA
                                 An independet project
 Método de Obtenção da Posição de Atirador
                              -------------------
        begin                : 2018-01-15
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

from Core.enums import Enums
from Core.DatabaseTools.DatabaseManager.databaseFactory import DatabaseFactory

class Settings(object):
    """
    Manages all MOPA's settings.
    """
    def __init__(self):
        """
        Class constructor.
        """
        super(Settings, self).__init__()
        if self.check():
            self.settingsDb = DatabaseFactory.getDatabase(
                                    self.defaultDriver(),
                                    self.getDefaultDatabaseConnectionParameter()
                                )
        else:
            self.setup()

    def check(self):
        """
        Checks if settings database is set.
        """
        # validate contents still to do - for now just check if it exists
        return os.path.exists(self.getDefaultDatabaseConnectionParameter()['path'])

    def defaultDriver(self):
        """
        Gets current default driver's name.
        :return: (str) default driver's name.
        """
        return Enums.SQLite3

    def getDefaultDatabaseConnectionParameter(self):
        """
        Gets default connection parameters for settings database.
        """
        return { 'path' : os.path.join(self.configPath(), 'databases', 'settings.db') }

    def configPath(self):
        """
        Gets default configuration's path.
        :return: (str) default path.
        """
        return os.path.dirname(__file__)

    def setupDatabases(self):
        """
        Sets up initial databases.
        :return: (bool) if databases are ready to use.
        """
        param = self.getDefaultDatabaseConnectionParameter()
        db = DatabaseFactory.getDatabase(self.defaultDriver(), {})
        db.createDatabase(param)
        db.connect(param)
        if db.isConnected():
            self.settingsDb = db
            db.createObservations()
            db.createSensors()
        else:
            return False
        # replace by settings validation method later
        return self.check()

    def setup(self):
        """
        Sets up initial configurations.
        """
        res = True
        res = res and self.setupDatabases()
        return res

    def addSensor(self, coordinates, epsg, status):
        """
        Add a new sensor to the database.
        :param coordinates: (tuple-of-floats) tuple with sensor's coordinates.
        :param epsg: (int) CRS authentication ID.
        :param status: (bool) sensor's activation status.
        """
        self.settingsDb.addSensor(coordinates, epsg, status)

    def getSensor(self, sensorId):
        """
        Gets a sensor info from database using its ID.
        :param sensorId: (int) sensor ID.
        :return: (tuple-of-values) sensor's information.
        """
        return self.settingsDb.getSensor(sensorId)

    def sensorsItems(self):
        """
        Gets all info form all sensors in the database.
        :return: (list-of-tuples) all sensors' informations.
        """
        return self.settingsDb.allSensors()
