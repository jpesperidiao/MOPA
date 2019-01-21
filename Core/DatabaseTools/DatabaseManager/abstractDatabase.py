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

import sqlite3, os
from PyQt5.QtCore import QObject

from Core.enums import Enums
from Core.DatabaseTools.SqlGenerator.sqlGeneratorFactory import SqlGeneratorFactory

class AbstractDatabase(QObject):
    def __init__(self, parameters=None):
        """
        Connects to a database and manages its contents.
        :parameters: (dict) connection parameters.
        """
        super(AbstractDatabase, self).__init__()
        self.connect(parameters)
        self.gen = self.sqlGenerator()

    def driver(self):
        """
        Gets current connection's driver.
        :return: (int) driver code/enum.
        """
        return Enums.NoDatabase

    def driverName(self):
        """
        Gets current connection's driver name.
        """
        return "NoDriver"

    def name(self):
        """
        Gets current database's connection name.
        :return: (str) database name.
        """
        return ''

    def query(self, sql, commit=False):
        """
        Executes a query on loaded database.
        :param sql: (str) SQL statement to be executed on the database.
        :param commit: (bool) if any changes should be commited to database.
        :return: (cursor?) cursor to query results. 
        """
        # to be reimplemented
        pass

    def validateConnectionParameters(self, parameters):
        """
        Validates connection parameters before trying to connect it.
        :parameters: (dict) connection parameters.
        :return: (bool) parameters' validity status.
        """
        # to be reimplemented
        return False

    def connect(self, parameters):
        """
        Connects to a database and sets it to db attribute.
        :parameters: (dict) connection parameters.
        :return: () database object.
        """
        # to be reimplemented
        self.db = None

    def isConnected(self):
        """
        Checks if current database is connected to a valid source.
        :return: (bool) validity status.
        """
        # to be reimplemented
        return self.db is not None

    def createDatabase(self, parameters):
        """
        Creates a database.
        :return: (bool) creation status.
        """
        # to be reimplemented
        return False

    def disconnect(self):
        """
        Disconnects from a database, if connected to any.
        """
        if self.db is not None:
            self.db.close()
            del self.db
            self.db = None

    def sqlGenerator(self):
        """
        Gets a SQL generator object.
        :return: (AbstractSqlGenerator) SQL generator.
        """
        return SqlGeneratorFactory.getGenerator(self.driver())

    def createObservations(self):
        """
        Creates observations table.
        :return: (bool) execution status.
        """
        self.query(self.gen.createObservations(), commit=True)
        return 'observation' in self.allTables()
    
    def createSensors(self):
        """
        Creates observations table.
        :return: (bool) execution status.
        """
        self.query(self.gen.createSensors(), commit=True)
        return 'sensors' in self.allTables()

    def allTables(self):
        """
        Gets a list of all available tables.
        :return: (list-of-str) list of names from available tables.
        """
        if self.isConnected():
            return [t[0] for t in self.query(self.gen.allTables())]
        return []

    def allObservations(self):
        """
        A list of all observation's information present at the database.
        :return: (list-of-tuple) observations' informations.
        """
        if self.isConnected():
            return self.query(self.gen.allObservations())
        return []

    def allSensors(self):
        """
        A list of all sensor's information present at the database.
        :return: (list-of-tuple) sensors' informations.
        """
        if self.isConnected():
            return self.query(self.gen.allSensors())
        return []

    def getSensor(self, sensorId):
        """
        Gets a sensor using its ID.
        :param sensorId: (int) sensor's ID.
        :return: (tuple) sensor's informations, if it exists.
        """
        if self.isConnected():
            sensorL = self.query(self.gen.getSensor(sensorId))
            return sensorL[0] if len(sensorL) > 0 else tuple()
        return tuple()

    def addObservation(self, azimuth, zenith, sensorId, commit=True):
        """
        Adds a sensor to the database.
        :param azimuth: observation's azimuth angle.
        :param zenith: observation's zenith angle.
        :param sensorId: (str) station's ID.
        :param commit: (bool) commit addition to database.
        """
        if self.isConnected():
            return self.query(self.gen.addObservation(azimuth, zenith, sensorId), commit)
        return 

    def addSensor(self, coordinates, epsg, name=None, status=True, commit=True):
        """
        Gets a sensor using its ID.
        :param coordinates: (tuple-of-float) sensor's coordinates.
        :param epsg: (int) sensor's CRS auth id.
        :param name: (str) station's friendly name.
        :param status: (bool) working status.
        :param commit: (bool) commit addition to database.
        """
        if self.isConnected():
            return self.query(self.gen.addSensor(coordinates, epsg, name, status), commit)
        return 

    def createShootersTable(self, tablename, commit=True):
        """
        Creates the shooters' table. Method should be invoked from settings module.
        :para tablename: (str) shooters' table name (default from settings).
        :param commit: (bool) commit table creation to the database.
        """
        if self.isConnected() and not self.tableExists(tablename):
            self.query(self.gen.createShootersTable(tablename), commit)
            return self.tableExists(tablename)
        return False

    def dropShootersTable(self, tablename, commit=True):
        """
        Drops shooters' table. Method should be invoked from settings module.
        :para tablename: (str) shooters' table name (default from settings).
        :param commit: (bool) commit table creation to the database.
        """
        if self.isConnected() and self.tableExists(tablename):
            self.query(self.gen.dropTable(tablename), commit)
            return not self.tableExists(tablename)
        return False

    def tableExists(self, tablename):
        """
        Verifies if table exists into database.
        :param tablename: (str) table's name.
        :return: (bool) whether table exists.
        """
        return tablename in self.allTables()
