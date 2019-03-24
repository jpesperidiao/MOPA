# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MOPA
                                 An independet project
 Método de Obtenção da Posição de Atirador
                              -------------------
        begin                : 2019-01-13
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

import numpy as np

from Settings.settings import Settings
from Core.Sensor.sensorsManager import SensorsManager
from Core.enums import Enums

class ShooterFinder():
    """
    Class designed to handle problem solving. It should be able to:
    1- provide a solution (shooter object) to a given observation along with a
       set of sensors distributed over a territory, represented by a raster dem.

    Important:
    It is assumed that the azimuth and zenith angles calculated by the sensor is 
    taking METRICAL units as reference when generating it! If not, this should be
    changed and somehow treated!

    How do the scripts find their solutions:
    1- define a region of interest based on maximum shooting range;
    2- calculate height for roi (possible points);
    3- verifies actual height and if it is within height tolerance; and
    4- filter possible solutions by a conical filter (angle tolerances). (optional)
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
            'alTol' : 0.2 * spatialResolution, # altimetric tolerance
            'angTol' : 1.5, # angular tolerance
            'maxDistance' : 1000., # maximum shooting's distance from sensor
            'scale' : 75, # exponential distribuition parameter (Helmert's method)
            'nrPoints' : 150 # number of points to be generated in Helmert's method
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

    def regionOfInterest(self, sensor, maxDistance):
        """
        Finds ROI around a sensor considering maximum distnace a shooter can be to it.
        :param sensor: (Sensor) target sensor.
        :param maxDistance: (float) maximum distance to which a shooter can be positioned in map units.
        :return: (tuple-of-floats) coordinates from ROI in the same form as 'extents'
                 method from RasterLayer.
        """
        y, x, _ = sensor['coordinates']
        return (x - maxDistance, x + maxDistance, y - maxDistance, y + maxDistance)

    def pixelRoi(self, dem, sensor, maxDistance):
        """
        Finds ROI in pixel coordinates from raster.
        :param spatialRes: (RasterLayer) DEM raster.
        :param sensor: (Sensor) target sensor.
        :param maxDistance: (float) maximum distance to which a shooter can be positioned in METERS.
        :return: (tuple-of-float) pixel coordinates for ROI.
        """
        if dem.isGeographic():
            maxDistance = maxDistance * 180 / (Enums.EARTH_RADIUS * Enums.PI)
        # y-axis is inverted because image's y-reference is inverted to normal axis
        xMin, xMax, yMax, yMin = self.regionOfInterest(sensor, maxDistance)
        xMin, yMin = dem.coordinatesToPixel(yMin, xMin)
        xMax, yMax = dem.coordinatesToPixel(yMax, xMax)
        return (max(0, xMin), min(dem.width(), xMax), max(0, yMin), min(dem.height(), yMax))

    def generateObservations(self, sensor, euclideanVector, scale=75, nrPoints=100):
        """
        Generates a set of pseudo-observations randomly from a given sensor. Uses
        an exponential distribuition of points definied by scale parameter to generate
        the random points.
        :param euclideanVector: (tuple-of-float) plane's euclidean vector.
        :param scale: (float) mean value for the exponential distribuition.
        :param nrPoints: (int) number of points to be generated.
        :return: (Numpy.array) and array of pseudo-observations.
        """
        # we are still using the parametric equation for a plane, so first thing is to do
        # is to generate a set of parameters
        parameters = np.random.exponential(scale, nrPoints)
        # from these parameters, we now use the sensor to get all generated points
        points = []
        ySensor, xSensor, zSensor = sensor['coordinates']
        for t in parameters:
            points.append([
                    xSensor + t * euclideanVector[0],
                    ySensor + t * euclideanVector[1],
                    zSensor + t * euclideanVector[2]
                ])
        return np.array(points)

    def helmertSolution(self, sensor, obs, dem, parameters):
        """
        Finds shooter's position using Helmert's parametrical adjustment of a plane defined by
        observation's azimuth (as its Euclidean vector) and the raster file.
        :param sensor: (Sensor) sensor that detected the shooter.
        :param obs: (Observation) observation's info.
        :param: (RasterLayer) digital elevation model from target area.
        :return: (Shooter) shooter's info.
        """
        altitudeTolerance = parameters['alTol']
        nrPoints = parameters['nrPoints']
        scale = parameters['scale']
        maxDistance = parameters['maxDistance']
        xMin, xMax, yMin, yMax = self.pixelRoi(dem, sensor, maxDistance)
        roi = dem.bands()[xMin:xMax, yMin:yMax]
        zen, az = obs['zenith'], obs['azimuth'] # in degrees
        zen = zen * np.pi / 180
        az = az * np.pi / 180
        euclideanVector = np.array([np.sin(zen) * np.cos(az), np.cos(zen) * np.cos(az), np.sin(az)])
        # generate a set of observations to use in Helmert's adjustment
        observations = self.generateObservations(sensor, euclideanVector, scale, nrPoints)
        # build helmert's matrices
        A = np.array([observations[:, 0], observations[:, 1], [1] * nrPoints]).transpose() # obs matrix
        B = observations[:, 2] # observation values vector (L1)
        C = np.array([sensor['coordinates'][1], sensor['coordinates'][2], 1]) # restriction vector
        # prepare extended matrix for Helmert's linear system of equations to be solved
        # the heights with restriction can be prepared now
        H = A.transpose().dot(B)
        H = [H[0], H[1], H[2], sensor['coordinates'][2]]
        M=[]
        A = A.transpose().dot(A)
        for i in range (0,3):
            M.append([A[i,0], A[i,1], A[i,2], C[i]])
        M.append([C[0], C[1], C[2], 0])
        M = np.array(M)
        # z = a0 * x + a1 * y + a2 
        a0, a1, a2, _ = np.linalg.solve(M,H) # solving for X in MX = H
        shooters = set()
        gt = dem.getGeoTransformParam()
        for col in range(xMin, xMax):
            for row in range(yMin, yMax):
                y, x = dem.pixelToCoordinates(col, row, gt)
                h = a0 * x + a1 * y + a2
                if abs(h - roi[col-xMin][row-yMin]) <= altitudeTolerance:
                    shooters.add((row, col, h))
        return shooters

    def findPlaneHeights(self, euclideanVector, roi, sensor, dem, lineTolerance):
        """
        Finds the heights for all pixels in ROI (e.g. the plane defined by euclidean vector for
        ROI points). Method used by analytical method. Parametrical plane equation: V1 = V2 + k*T.
        :param euclideanVector: (tuple-of-float) euclidenan vector's azimuth and zenith angles.
        :param roi: (Numpy.nparray) region in DEM that should be searched.
        :param dem: (RasterLayer) region where event is contained.
        :param lineTolerance: (float) tolerance value to which a distortion of a point from a line
                              may consider it part of it ("snap radius").
        :return: (Numpy.ndarray) array heights (plane defined by E.V. in ROI).
        """
        geoTransformParam = dem.getGeoTransformParam()
        sensorY, sensorX, sensorZ = sensor['coordinates']
        heights = np.zeros(roi.shape)
        if dem.isGeographic():
            # considering that observation takes distance as its unit when being processed by sensor
            sensorY = np.deg2rad(sensorY) * Enums.EARTH_RADIUS
            sensorX = np.deg2rad(sensorX) * Enums.EARTH_RADIUS
        for lin in range(len(roi)):
            for col in range(len(roi[0])):
                y, x = dem.pixelToCoordinates(col, lin, geoTransformParam)
                # "directional" plane parameter
                tx, ty = 0, 0
                if dem.isGeographic():
                    y = np.deg2rad(y) * Enums.EARTH_RADIUS
                    x = np.deg2rad(x) * Enums.EARTH_RADIUS
                if euclideanVector[0] != 0:
                    tx = (x - sensorX) / euclideanVector[0]
                if euclideanVector[1] != 0:
                    ty = (y - sensorY) / euclideanVector[1]
                t = np.sqrt((tx ** 2 + ty ** 2) * .5) if tx > 0 and ty > 0 \
                    else -np.sqrt((tx ** 2 + ty ** 2) * .5)
                if np.sqrt(((t - tx) ** 2 + (t - ty) ** 2) * .5) / t <= lineTolerance:
                    heights[lin][col] = sensorZ + t * euclideanVector[2]
                else:
                    # some unrealistic height
                    heights[lin][col] = 9999.0
        return heights

    def analyticalSolution(self, sensor, obs, dem, parameters):
        """
        Finds shooter's position using Analytical method. Method developped by me and my team
        for undergrad's final project. Also uses the observation azimuth as a the Euclidean vector
        of the plane that contains both shooter and sensor and intersects its plane with the DEM.
        :param sensor: (Sensor) sensor that detected the shooter.
        :param obs: (Observation) observation's info.
        :param dem: (RasterLayer) digital elevation model from target area.
        :return: (Shooter) shooter's info.
        """
        zen, az = obs['zenith'], obs['azimuth'] # in degrees
        zen = zen * np.pi / 180
        az = az * np.pi / 180
        euclideanVector = np.array([np.sin(zen) * np.cos(az), np.cos(zen) * np.cos(az), np.sin(az)])
        angTol = parameters['angTol']
        maxDistance = parameters['maxDistance']
        altitudeTolerance = parameters['alTol']
        # 0.5 was arbitrarily used before
        # lineTol = angTol / maxDistance
        lineTol = 0.1
        xMin, xMax, yMin, yMax = self.pixelRoi(dem, sensor, maxDistance)
        roi = dem.bands()[xMin:xMax, yMin:yMax]
        planeHeights = self.findPlaneHeights(euclideanVector, roi, sensor, dem, lineTol)
        shooters = set()
        for row in range(len(roi)):
            for col in range(len(roi[0])):
                h = planeHeights[row][col]
                if abs(h - roi[row][col]) <= altitudeTolerance:
                    # minimum coordinates must be added to map it back to original raster px coordinates
                    shooters.add((row + yMin, col + xMin, h))
        return shooters

    def combinedSolution(self, sensor, obs, dem, parameters):
        """
        Combines Analytical and Helmert solutions.
        :param sensor: (Sensor) sensor that detected the shooter.
        :param obs: (Observation) observation's info.
        :param: (RasterLayer) digital elevation model from target area.
        :return: (Shooter) shooter's info.
        """
        return self.analyticalSolution(sensor, obs, dem, parameters) &\
               self.helmertSolution(sensor, obs, dem, parameters)
