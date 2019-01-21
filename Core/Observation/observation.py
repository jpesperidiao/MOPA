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

from Settings.settings import Settings

class Observation(QObject):
    """
    I think a class parent to this and sensor should be implemented.
    (Something like QgsFeature for QGIS API, in order to make each children
    a specific application of it). Validation method is pretty much not enough.
    Some regex to check dates should be added, for instance...
    """
    def __init__(self, parameters):
        """
        Class constructor.
        :param parameters: (dict) observation's parameters map.
        """
        super(Observation, self).__init__()
        if self.validateParameters(parameters):
            self.parameters = parameters
        else:
            self.parameters = {
                'id' : None,
                'azimuth' : 0.,
                'zenith' : 0,
                'sensorId' : None,
                'date' : ''
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
        if 'azimuth' not in parameters or not isinstance(parameters['azimuth'], float) or \
                isinstance(parameters['azimuth'], float) > 180 or \
                isinstance(parameters['azimuth'], float) < -180:
            return self.tr("Invalid azimuth angle.")
        if 'zenith' not in parameters or not isinstance(parameters['zenith'], float) or \
                isinstance(parameters['zenith'], float) > 360 or \
                isinstance(parameters['zenith'], float) < 0:
            return self.tr("Invalid zenith angle.")
        if 'sensorId' not in parameters or not isinstance(parameters['sensorId'], int): # or \
                # not Settings().getSensor(parameters['sensorId']).isValid():
            # it checks if sensor associated exists into database before adding obs to db
            return self.tr("Invalid sensor ID.")
        if 'date' not in parameters or \
                type(parameters['date']) not in (type(None), str):
            return self.tr("Invalid event date.")
        return ""

    def validateParameters(self, parameters):
        """
        Validates sensor's parameters map.
        :param parameters: (dict) parameters map.
        :return: (bool) validity status.
        """
        return self.invalidationReason(parameters) == ""
