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
        Get all available tables from database.
        """
        return ""
