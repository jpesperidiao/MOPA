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

class AbstractSqlGenerator():
    def __init__(self):
        pass

    def createObservations(self):
        """
        Creates the observations (shooting events) table.
        """
        return ""

    def createSensors(self):
        """
        Creates the sensors (sensors positions and working info) table.
        """
        return ""

    def allTables(self):
        """
        Gets all available tables in the database.
        """
        return ""

    def allObservations(self):
        """
        Gets all observations from database.
        """
        return ""

    def allSensors(self):
        """
        Gets all sensors from database.
        """
        return ""

    def getObservation(self, obsId):
        """
        Gets a observation using its ID.
        :param obsId: (int) observation's ID.
        """
        return ""

    def getSensor(self, sensorId):
        """
        Gets a sensor using its ID.
        :param sensorId: (int) sensor's ID.
        """
        return ""

    def addObservation(self, azimuth, zenith, sensorId):
        """
        Adds a sensor to the database.
        :param azimuth: observation's azimuth angle.
        :param zenith: observation's zenith angle.
        :param sensorId: (str) station's ID.
        """
        return ""

    def addSensor(self, coordinates, epsg, name=None, status=True):
        """
        Adds a sensor to the database.
        :param coordinates: (tuple-of-float) new sensor's coordinates.
        :param epsg: (int) auth id for coordinates' CRS.
        :param name: (str) station's friendly name.
        :param status: (bool) sensor's activation status.
        """
        return ""

    def dropTable(self, tablename):
        """
        Drops table from database.
        :param tablename: (str) table to be dropped
        """
        return ""

    def createShootersTable(self, tablename):
        """
        Creates the shooters' table.
        :para tablename: (str) shooters' table name (default from settings).
        """
        return ""
