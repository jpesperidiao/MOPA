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

from Core.enums import Enums
from .SupportedDrivers.sqliteDatabase import SqliteDatabase

class DatabaseFactory:
    @staticmethod
    def getDatabase(driver, parameters):
        """
        Gets an SQL generator accordingly to its driver.
        :param driver: (int) driver code/enum.
        """
        return {
            Enums.NoDatabase : lambda : None,
            Enums.SQLite3 : lambda : SqliteDatabase(parameters)
        }[driver]() if driver <= Enums.TotalDatabaseDrivers and driver >= 0 else None