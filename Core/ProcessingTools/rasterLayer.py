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
        :param: (str) path to raster file.
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
        return None if self.dataset() is None else self.dataset().ReadAsArray()

    def width(self):
        """
        Gets raster X length (raster's width).
        :return: (int) raster's width.
        """
        return len(self.bands()[0]) if self.dataset() is not None else 0

    def height(self):
        """
        Gets raster X length (raster's height).
        :return: (int) raster's height.
        """
        return len(self.bands()) if self.dataset() is not None else 0

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
