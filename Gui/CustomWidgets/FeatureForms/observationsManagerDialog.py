# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MOPA
                                 An independet project
 Método de Obtenção da Posição de Atirador
                              -------------------
        begin                : 2019-03-06
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
from Gui.CustomWidgets.FeatureForms.featureForm import FeatureForm

class ObservationsManagerDialog():
    def __init__(self, settings=None, parent=None):
        """
        Class constructor.
        :param settings: (Settings) MOPA's settings object.
        :param parent: (QWidget) widget to wich this object is related to.
        """
        self.settings = settings if settings is not None else Settings()
        self.parent = parent
        self._observationManager = ObservationsManager(settings)

    def openForm(self, obs=None, isEditable=True):
        """
        Opens attribute form for a given observation. Updates observation if necessary.
        :param obs: (Observation) the observation to have its attributes exposed.
        :param isEditable: (bool) indicates whether attributes may be updated.
        """
        if obs is None:
            obs = self._observationManager.newObservation()
            isEditable = True
        form = FeatureForm(obs, isEditable, self.parent)
        # form.setTitle(form.tr("Observation Attributes Form - add new observation"))
        if form.exec_() and isEditable:
            # updates observations contents if form was updated and is on editing mode
            attributes = form.read()
            # maybe raise a message box to confirm any overwriting?
            self._observationManager.updateObservation(attributes)
