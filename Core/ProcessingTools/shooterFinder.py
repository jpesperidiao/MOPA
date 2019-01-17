# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MOPA
                                 An independet project
 Método de Obtenção da Posição de Atirador
                              -------------------
        begin                : 2018-01-13
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
from Core.Sensor.sensorsManager import SensorsManager

class ShooterFinder():
    """
    Class designed to handle problem solving. It should be able to:
    1- provide a solution (shooter object) to a given observation along with a
       set of sensors distributed over a territory, represented by a raster dem.
    """
    # methods enumerator
    AvailableMethods = 3
    Helmert, Analytical, Combined = list(range(AvailableMethods))

    def __init__(self, settings=None):
        """
        Class constructor.
        """
        if settings is None:
            settings = Settings()
        self.settings = settings
        self.setupView()

    def setupView(self):
        """
        Sets up the shooters table view into settings database. It clears it up in case
        of existing data on it.
        :return: (bool) view working status.
        """
        return self.settings.clearShootersView()

    def defaultParameters(self, spatialResolution):
        """
        Gets default parameters for the methods. Some parameters have its value dependent to
        the DEM's spatial resolution as the precision from the algorithm is directly affected
        by it.
        :param spatialResolution: (int) DEM's spatial resolution.
        """
        return {
            'plTol' : 0.05 * spatialResolution, # planimetric tolerance
            'alTol' : 0.01 * spatialResolution, # altimetric tolerance
            'angTol' : 5. # angular tolerance
        }

    def findShooter(self, method, sensor, obs, dem, parameters=None):
        """
        Finds the shooter's position from an observation made by a sensor.
        :param method: (int) method code/enum.
        :param sensor: (Sensor) sensor that detected the shooter.
        :param obs: (Observation) observation's info.
        :param: (RasterLayer) digital elevation model from target area.
        :return: (Shooter) shooter's info.
        """
        if parameters is None:
            parameters = self.defaultParameters(dem.spatialResolution())
        return {
            ShooterFinder.Helmert : self.helmertSolution,
            ShooterFinder.Analytical : self.analyticalSolution,
            ShooterFinder.Combined : self.combinedSolution
        }[method](sensor, obs, dem, parameters)

    def helmertSolution(self, sensor, obs, dem, parameters):
        """
        Finds shooter's position using Helmert's parametrical adjustment of a plane defined by
        observation's azimuth (as its Euclidean vector) and the raster file.
        :param sensor: (Sensor) sensor that detected the shooter.
        :param obs: (Observation) observation's info.
        :param: (RasterLayer) digital elevation model from target area.
        :return: (Shooter) shooter's info.
        """
        # TODO
        return None

    def analyticalSolution(self, sensor, obs, dem, parameters):
        """
        Finds shooter's position using Analytical method. Method developped by me and my team
        for undergrad's final project. Also uses the observation azimuth as a the Euclidean vector
        of the plane that contains both shooter and sensor and intersects its plane with the DEM.
        :param sensor: (Sensor) sensor that detected the shooter.
        :param obs: (Observation) observation's info.
        :param: (RasterLayer) digital elevation model from target area.
        :return: (Shooter) shooter's info.
        """
        # TODO
        return None

    def combinedSolution(self, sensor, obs, dem, parameters):
        """
        Combines Analytical and Helmert solutions.
        :param sensor: (Sensor) sensor that detected the shooter.
        :param obs: (Observation) observation's info.
        :param: (RasterLayer) digital elevation model from target area.
        :return: (Shooter) shooter's info.
        """
        # TODO
        return None
