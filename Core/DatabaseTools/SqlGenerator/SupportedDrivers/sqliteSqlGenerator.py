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

from Core.DatabaseTools.SqlGenerator.abstractSqlGenerator import AbstractSqlGenerator

class SqliteSqlGenerator(AbstractSqlGenerator):
    def __init__(self):
        """
        Class constructor.
        """
        super(SqliteSqlGenerator, self).__init__()
        
    def createTable(self, tablename, columnMap, pk=None, fkMap=None):
        """
        Gets query to create a table.
        :param tablename: (str) table name.
        :param columnMap: (dict) column names mapped to its type.
        :param fkMap: (dict) maps foreign key to its external table and its column.
        :return: (str) query for table creation
        """
        columnString = ""
        for col, colType in columnMap.items():
            if col == pk:
                columnString = ", \n".join(
                                    (
                                        columnString,
                                        "{col} {colType} PRIMARY KEY".format(col=col, colType=colType)
                                    )
                                )
            else:
                columnString = ", \n".join(
                                    (
                                        columnString,
                                        "{col} {colType}".format(col=col, colType=colType)
                                    )
                                )
        if fkMap is not None:
            for fk, (table, col) in fkMap.item():
                ", \n".join(
                        (
                            columnString,
                            "FOREIGN KEY ({fk}) REFERENCES {table}({col})".format(fk=fk, col=col, table=table)
                        )
                    )
        return "CREATE TABLE {table} ({columns});".format(table=tablename, columns=columnString)

    def createObservations(self):
        """
        Creates the observations (shooting events) table.
        """
        return """\
        CREATE TABLE observations (
            id INTEGER PRIMARY KEY,
            angle TEXT NOT NULL,
            sensor INTEGER NOT NULL,
            date TIMESTAMP,
            FOREIGN KEY(sensor) REFERENCES sensors(id)
        )
        """

    def createSensors(self):
        """
        Creates the sensors (sensors positions and working info) table.
        """
        return """\
        CREATE TABLE sensors (
            id INTEGER PRIMARY KEY,
            coordinates TEXT NOT NULL,
            epsg INTEGER NOT NULL,
            activation_date TIMESTAMP,
            deactivation_date TIMESTAMP,
            status BOOLEAN
        )
        """

    def allTables(self):
        """
        Gets all available tables in the database.
        """
        return "SELECT tbl_name FROM sqlite_master;"
