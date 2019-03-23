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

import math

class Enums:
    # database drivers enumerates
    TotalDatabaseDrivers = 1
    NoDatabase, SQLite3 = list(range(TotalDatabaseDrivers + 1))
    # execution codes
    Finished, FinishedWithErrors, Cancelled = list(range(3))
    # approximation of earth radius in meters
    EARTH_RADIUS = 6378100
    PI = math.pi
    # default push buttons
    OkButton, CancelButton = list(range(2))