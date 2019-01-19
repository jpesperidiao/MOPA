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

    How do the scripts find their solutions:
    1- define a region of interest based on maximum shooting range;
    2- 
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
            'angTol' : 1.5, # angular tolerance
            'maxDistance' : 1000. # maximum shooting's distance from sensor
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

    def regionOfInterest(posRec, dataset, resolEspacial, distMaxDisparo=1000.0):
        """
        Finds ROI inside dem area in order to avoid unnecessary calculations.
        TO DETERMINE PARAMETERS STILL - METHOD JUST COPIED FROM ORIGINAL SCRIPT
        :return: (tuple-of-floats) coordinates from ROI in the same form as 'extents'
                 method from RasterLayer.
        """
        gt = dataset.GetGeoTransform()
        elevation = dataset.ReadAsArray()
        limiteDisparo = int((distMaxDisparo / resolEspacial)) # para limitar por regiao de real possibilidade de disparo
        xMax = len(elevation)
        yMax = len(elevation[0])
        
        # converter coordenadas de campo para pixel
        denominador = 1. / (gt[1] * gt[5] - gt[2] * gt[4])
        px = int((gt[5] * (posRec[0] - gt[0]) - gt[2] * (posRec[1] - gt[3])) * denominador - 0.5)
        py = int(-(gt[4] * (posRec[0] - gt[0]) - gt[1] * (posRec[1] - gt[3])) * denominador - 0.5)
        
        (xMin, xMax, yMin, yMax) = (max(0, px - limiteDisparo), min(xMax, px + limiteDisparo), 
                                    max(0, py - limiteDisparo), min(yMax, py + limiteDisparo))
        
        return (int(xMin), int(xMax), int(yMin),int(yMax))

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
