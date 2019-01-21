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

import os, gdal, osr
import numpy as np

from Core.enums import Enums

class RasterLayer(object):
    def __init__(self, path=None):
        """
        Class constructor.
        :param path: (str) path to raster file.
        """
        super(RasterLayer, self).__init__()
        self.gdalDataset = self.getGdalDataset(path)
        self.directory = path

    def name(self):
        """
        Gets raster name from GeoTIFF filename.
        :return: (str) raster layer name.
        """
        return os.path.basename(os.path.splitext(self.directory)[0]) if self.directory is not None else ""

    def getGdalDataset(self, path):
        """
        Gets GDAL dataset.
        :param path: (str) path to raster.
        :return: (GDALDatasetShadow) GDAL dataset.
        """
        return gdal.Open(path) if path is not None else None

    def setRaster(self, path):
        """
        Resets layer to new raster path.
        :param path: (str) new raster path.
        """
        if self.dataset() is not None:
            del self.gdalDataset
        self.directory = path
        self.gdalDataset = self.getGdalDataset(path)

    def dataset(self):
        """
        Gets current GDAL dataset loaded to object.
        :return: (GDALDatasetShadow) GDAL dataset.
        """
        return self.gdalDataset

    def bands(self):
        """
        Gets raster bands as Numpy array.
        :return: (Numpy.ndarray) raster's bands.
        """
        return np.array([[]]) if self.dataset() is None else self.dataset().ReadAsArray()

    def bandCount(self):
        """
        Gets the number of bands on raster.
        :return: (int) 
        """
        return self.dataset().RasterCount if self.dataset() is not None else 0

    def width(self):
        """
        Gets raster X length (raster's width).
        :return: (int) raster's width.
        """
        return self.dataset().RasterXSize if self.dataset() is not None else 0

    def height(self):
        """
        Gets raster X length (raster's height).
        :return: (int) raster's height.
        """
        return self.dataset().RasterYSize if self.dataset() is not None else 0

    def isValid(self):
        """
        Gets current raster file selection's validity status.
        :return: (bool) validity status.
        """
        return self.width() != 0 and self.height() != 0

    def epsg(self):
        """
        Gets raster's EPSG authentication ID.
        :return: (int) EPSG auth ID.
        """
        try:
            return int(self.dataset().GetProjection().split(',')[-1].split('"')[1])
        except:
            return 0

    def isProjected(self):
        """
        Determines whether raster has a projected CRS.
        :return: (bool) if raster is projected.
        """
        if self.dataset() is None:
            return False
        srs = osr.SpatialReference(wkt=self.dataset().GetProjetion())
        return bool(srs.IsProjected())

    def isGeographic(self):
        """
        Determines whether raster has a geographic CRS.
        :return: (bool) if raster is projected.
        """
        if self.dataset() is None:
            return False
        srs = osr.SpatialReference(wkt=self.dataset().GetProjection())
        return bool(srs.IsGeographic())

    def projection(self):
        """
        Gets projection information from a GDAL dataset. If no information is found from image,
        empty string is returned.
        :return: (str) projection string.
        """
        try:
            return '{0} (EPSG:{1})'.format(self.dataset().GetProjection().split(',')[0].split('"')[1],\
                                self.epsg())
        except:
            return ''

    def getGeoTransformParam(self):
        """
        Gets geotransformation parameters.
        0: px
        :return: (list-of-float) list of geotransformation parameters.
        """
        try:
            return self.dataset().GetGeoTransform()
        except:
            return [0., 0., 0., 0., 0., 0.]

    def spatialResolution(self):
        """
        Gets raster's spatial resolution. For geographic coordinates an aproximation is used.
        Considering the aproximations used, it is highly counter-recommended to use rasters using geographical
        coordinate systems.
        :return: (float) raster's spatial resolution in meters (cell size).
        """
        try:
            pxWidth = abs(self.getGeoTransformParam()[1])
            if not self.isGeographic():
                # considering that no DEM with spatial resolution lesser than 0.01 m would be used,
                # which is safe to consider, it is considered, then, that pixelWidth is in degrees 
                return pxWidth
            else:
                # in order to retrieve spatial resolution, it is also considered the most common ones: 1, 5, 10, 30, 90
                possibleResList = [1, 5, 10, 30, 90]
                # aproximate resolution is retrieve as of PI * EARTH_RADIUS * ANGLE / 180
                aproxReso = np.pi * Enums.EARTH_RADIUS * pxWidth / 180
                if aproxReso > max(possibleResList):
                    return max(possibleResList)
                for idx, reso in enumerate(possibleResList):
                    if aproxReso < reso:
                        if idx == 0:
                            # must check with both limits
                            return reso
                        if abs(reso - aproxReso) > (possibleResList[idx - 1] - reso):
                            return possibleResList[idx - 1]
                        else:
                            return reso
        except:
            return 0

    def pixelToCoordinates(self, col, lin, gt=None):
        """
        Gets the coordinates of a given pixel. It is considered pixel center.
        :param col: (int) pixel column.
        :param lin: (int) pixel line.
        :param gt: (list-of-float) dataset's geotransformation parameters.
        :return: (tuple-of-float) X and Y coordinates (may be in meters/degrees/etc, defined by entry)
        """
        if col > self.width() or lin > self.height():
            return (.0, .0)
        if gt is None:
            gt = self.getGeoTransformParam()
        coordY = gt[3] + (col + 0.5)*gt[4] + (lin + 0.5)*gt[5] 
        coordX = gt[0] + (col + 0.5)*gt[1] + (lin + 0.5)*gt[2]
        return (coordY, coordX)

    def coordinatesToPixel(self, yValue, xValue, gt=None):
        """
        Gets pixel column and line from its coordinates. Returns (-1, -1), if coordinates are out of bounds.
        :param xValue: (float) x coordinate (may be lat/long, meters or whatever).
        :param yValue: (float) y coordinate (may be lat/long, meters or whatever).
        :return: (tuple-of-int) column and line for given coordinates.
        """
        if gt is None:
            gt = self.getGeoTransformParam()
        denominator = gt[1] * gt[5] - gt[2] * gt[4]
        if denominator == 0.:
            return (-1, -1)
        denominator = 1 / denominator
        x = xValue - gt[0]
        y = yValue - gt[3]
        col = int((gt[5] * x - gt[2] * y) * denominator)
        col = col if col <= self.height() else -1
        lin = int((-1 * gt[4] * x + gt[1] * y) * denominator)
        lin = lin if lin <= self.width() else -1
        return (col, lin)

    def extents(self):
        """
        Gets raster's bounding box. The order is: minimum X, maximum X, minimum Y and maximum Y.
        :return: (tuple-of-floats) raster's extents.
        """
        if self.isValid():
            xMin, dx, rotX, yMax, rotY, dy = self.getGeoTransformParam()
            xMax = xMin + dx * self.width() + rotX * self.height()
            yMin = yMax + dy * self.height() + rotY * self.width()
            return xMin, xMax, yMin, yMax
        else:
            return [0., 0., 0., 0.]

    def hasPoint(self, coordinates):
        """
        Checks if a point (tuple of coordinates) is contained by rasters extents.
        :param coordinate: (tuple-of-floats) coordinates from point to be checked.
        :return: (bool) whether points is inside raster's area.
        """
        if not self.isValid():
            return False
        xMin, xMax, yMin, yMax = self.extents()
        # Z is optional.
        y, x = coordinates[0], coordinates[1]
        return (x >= xMin and x <= xMax) and (y >= yMin and y <= yMax)

    def rasterValueFromPoint(self, coordinates):
        """
        Requests raster's value from a point.
        :param coordinate: (tuple-of-floats) coordinates from point to be checked.
        :return: (list-of-float) whether points is inside raster's area.
        """
        if not (self.isValid() and self.hasPoint(coordinates)):
            return []
        col, lin = self.coordinatesToPixel(coordinates[0], coordinates[1])
        if self.bandCount() > 1:
            return [band[lin][col] for band in self.bands()]
        else:
            return [self.bands()[lin][col]]
