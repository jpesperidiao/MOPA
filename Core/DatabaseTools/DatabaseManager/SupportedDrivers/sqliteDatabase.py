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

from Core.enums import Enums
from Core.DatabaseTools.DatabaseManager.abstractDatabase import AbstractDatabase

class SqliteDatabase(AbstractDatabase):
    def __init__(self, parameters=None):
        """
        Connects to a database and manages its contents.
        :parameters: (dict) connection parameters.
        """
        super(SqliteDatabase, self).__init__(parameters)

    def driver(self):
        """
        Gets current connection's driver.
        :return: (int) driver code/enum.
        """
        return Enums.SQLite3

    def driverName(self):
        """
        Gets current connection's driver name.
        """
        return "SQLite3"

    def name(self):
        """
        Gets current database's connection name.
        :return: (str) database name.
        """
        return ''

    def invalidConnectionReason(self, parameters):
        """
        Gets the connection's invalidation reason.
        :parameters: (dict) connection parameters.
        :return: (str) parameters' invalidation reason.
        """
        if "path" not in parameters:
            return self.tr('Path to database was not given.')
        if not isinstance(parameters["path"], str):
            return self.tr("Path parameter is not a valid string path to a SQLite database.") 
        if not os.path.exists(parameters["path"]):
            return self.tr("{path} does not exists.").format(**parameters)
        if os.path.splitext(parameters["path"])[1] not in [".db", ".sqlite"]:
            return self.tr("{path} does not have an .SQLITE extension.").format(**parameters)
        return ""

    def validateConnectionParameters(self, parameters):
        """
        Validates connection parameters before trying to connect it.
        :parameters: (dict) connection parameters.
        :return: (bool) parameters' validity status.
        """
        return self.invalidConnectionReason(parameters) == ""

    def connect(self, parameters):
        """
        Connects to a database and sets it to db attribute.
        :parameters: (dict) connection parameters.
        :return: () database object.
        """
        if self.validateConnectionParameters(parameters):
            try:
                self.db = sqlite3.connect(parameters['path'])
            except:
                self.db = None
        else:
            self.db = None

    def query(self, sql, commit=False):
        """
        Executes a query on loaded database.
        :param sql: (str) SQL statement to be executed on the database.
        :param commit: (bool) if any changes should be commited to database.
        :return: (list) query results.
        """
        if self.isConnected():
            cur = self.db.cursor()
            cur.execute(sql)
            if commit:
                self.db.commit()
            return cur.fetchall()
        return

    def createDatabase(self, parameters):
        """
        Creates an empty database.
        :return: (bool) creation status.
        """
        if os.path.exists(parameters["path"]):
            return False
        """ create a database connection to a SQLite database """
        try:
            conn = sqlite3.connect(parameters["path"])
            conn.close()
        except Exception as e:
            print(e)
        return os.path.exists(parameters["path"])
