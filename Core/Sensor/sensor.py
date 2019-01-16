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

from PyQt5.QtCore import QObject

class Sensor(QObject):
    def __init__(self, parameters):
        """
        Class constructor.
        """
        super(Sensor, self).__init__()
        if self.validateParameters(parameters):
            self.parameters = parameters
        else:
            self.parameters = {
                'id' : -1,
                'coordinates' : (0., 0.),
                'epsg' : 0,
                'activation_date' : '',
                'deactivation_date' : '',
                'status' : False
            }

    def __getitem__(self, key):
        """
        Makes sensor object work as a dict towards its parametric attributes.
        """
        return self.parameters[key] if key in self.parameters else None

    def invalidationReason(self, parameters):
        """
        Gets sensor's parameters map invalidation reason, if any.
        :param parameters: (dict) parameters map.
        :return: (str) invalidation reason.
        """
        if not isinstance(parameters, dict):
            return self.tr("Invalid parameters. It must be a map.")
        if 'id' not in parameters or not isinstance(parameters['id'], int):
            return self.tr("Invalid ID.")
        if 'coordinates' not in parameters or type(parameters['coordinates']) not in (list, tuple)\
            or not sum([type(coordinate) in (int, float) for coordinate in parameters['coordinates']]):
            return self.tr("Invalid coordinates.")
        if 'activation_date' not in parameters or not isinstance(parameters['activation_date'], str):
            return self.tr("Invalid activation date.")
        if 'deactivation_date' not in parameters or not isinstance(parameters['deactivation_date'], str):
            return self.tr("Invalid activation date.")
        if 'status' not in parameters or not isinstance(parameters['status'], bool):
            return self.tr("Invalid status.")
        return ""

    def validateParameters(self, parameters):
        """
        Validates sensor's parameters map.
        :param parameters: (dict) parameters map.
        :return: (bool) validity status.
        """
        return self.invalidationReason(parameters) == ""
