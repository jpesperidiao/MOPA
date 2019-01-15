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

import os, gdal
import numpy as np

class RasterLayer(object):
    # approximation of earth radius in meters
    EARTH_RADIUS = 6378100
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
            if pxWidth > 0.01:
                # considering that no DEM with spatial resolution lesser than 0.01 m would be used,
                # which is safe to consider, it is considered, then, that pixelWidth is in degrees 
                return pxWidth
            else:
                # in order to retrieve spatial resolution, it is also considered the most common ones: 1, 5, 10, 30, 90
                possibleResList = [1, 5, 10, 30, 90]
                # aproximate resolution is retrieve as of PI * EARTH_RADIUS * ANGLE / 180
                aproxReso = np.pi * self.EARTH_RADIUS * pxWidth / 180
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
        if col > self.height() or lin > self.width():
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
