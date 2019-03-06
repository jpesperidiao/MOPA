# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MOPA
                                 An independet project
 Método de Obtenção da Posição de Atirador
                              -------------------
        begin                : 2018-03-06
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

from Settings.settings import Settings
from Core.Observation.observationsManager import ObservationsManager
from Gui.CustomWidgets.featureForm import FeatureForm

class ObservationsManagerDialog():
    def __init__(self, settings=None, parent=None):
        """
        Class constructor.
        :param settings: (Settings) MOPA's settings object.
        :param parent: (QWidget) widget to wich this object is related to.
        """
        self.settings = settings if settings is not None else Settings()
        self._observationManager = ObservationsManager(settings)

    def observation(self, obsId):
        """
        Gets an observation from the database given its ID.
        :param obsId: (int) a observation ID.
        :return: (Observation) the onservation object.
        """
        return self._observationManager.newObservation()
