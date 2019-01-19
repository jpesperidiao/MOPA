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
                'id' : None,
                'name' : '',
                'coordinates' : (0., 0.),
                'epsg' : 0,
                'activation_date' : '',
                'deactivation_date' : '',
                'status' : False
            }

    def __getitem__(self, key):
        """
        Makes sensor object work as a dict towards its parametric attributes.
        :param key: (str) attribute name.
        :return: attribute value.
        """
        return self.parameters[key] if key in self.parameters else None

    def __str__(self):
        """
        When print is called, parameters will be exposed.
        """
        return str(self.parameters)

    def invalidationReason(self, parameters):
        """
        Gets sensor's parameters map invalidation reason, if any.
        :param parameters: (dict) parameters map.
        :return: (str) invalidation reason.
        """
        if not isinstance(parameters, dict):
            return self.tr("Invalid parameters. It must be a map of attributes.")
        if 'id' not in parameters or not isinstance(parameters['id'], int):
            return self.tr("Invalid ID.")
        if 'name' not in parameters or \
                type(parameters['name']) not in (type(None), str):
            return self.tr("Invalid sensor's base friendly name.")
        if 'coordinates' not in parameters or type(parameters['coordinates']) not in (list, tuple)\
            or not sum([type(coordinate) in (int, float) for coordinate in parameters['coordinates']]):
            return self.tr("Invalid coordinates.")
        if 'epsg' not in parameters or not isinstance(parameters['epsg'], int):
            return self.tr("Invalid CRS (EPSG code is not valid).")
        if 'activation_date' not in parameters or \
                type(parameters['activation_date']) not in (type(None), str):
            return self.tr("Invalid activation date.")
        if 'deactivation_date' not in parameters or \
                type(parameters['deactivation_date']) not in (type(None), str):
            return self.tr("Invalid deactivation date.")
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

    def isValid(self):
        """
        Checks if current instance has a valid set of parameters.
        :return: (bool) instance's validity status.
        """
        return self.validateParameters(self.parameters)
