# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MOPA
                     An independet project
 Método de Obtenção da Posição de Atirador
                  -------------------
     begin          : 2019-03-15
     git sha        : $Format:%H$
     copyright         : (C) 2019 by João P. Esperidião
     email          : joao.p2709@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                           *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                    *
 *                                           *
 ***************************************************************************/
"""

import os
from osgeo import osr

class GeoprocessingTools:
    """
    Class designed to contain all algs and methods for generic geoprocessing operations.
    """
    @staticmethod
    def epsgToWkt(epsg):
        """
        Gets the WKT from a EPSG.
        """
        return os.popen("gdalsrsinfo -o wkt epsg:{epsg}".format(epsg=epsg)).read()

    @staticmethod
    def srsFromEpsg(epsg):
        """
        Gets GDAL's spatial reference system object from authentication ID.
        :param epsg: (int) CRS' auth ID.
        :return: (osr.SpatialReference) OGR SRS object.
        """
        return osr.SpatialReference(GeoprocessingTools.epsgToWkt(epsg))

    @staticmethod
    def isProjected(epsg):
        """
        Determines whether raster has a projected CRS.
        :param epsg: (int) CRS' auth ID.
        :return: (bool) if CRS is projected.
        """
        srs = osr.SpatialReference(wkt=GeoprocessingTools.epsgToWkt(epsg))
        return bool(srs.IsProjected())

    @staticmethod
    def isGeographic(epsg):
        """
        Determines whether raster has a geographic CRS.
        :param epsg: (int) CRS' auth ID.
        :return: (bool) if CRS is projected.
        """
        srs = osr.SpatialReference(wkt=GeoprocessingTools.epsgToWkt(epsg))
        return bool(srs.IsGeographic())

    @staticmethod
    def projectionFromEpsg(epsg):
        """
        Gets the projection name from its authentication ID.
        :param epsg: (int) CRS' auth ID.
        :return: (str) projection's name.
        """
        # TODO
        return ""

    @staticmethod
    def coordinateTransformer(inputEpsg, outputEpsg):
        """
        Gets a OSR coordinate transformer object.
        :param inputCrs: (int) auth ID for input CRS.
        :param outputCrs: (int) auth ID for output CRS.
        :return: () coordinate transformer.
        """
        # TODO
        return osr.CoordinateTransformation(
            GeoprocessingTools.srsFromEpsg(inputEpsg),
            GeoprocessingTools.srsFromEpsg(outputEpsg)
        )

    @staticmethod
    def reprojectDataset(dataset, outputCrs):
        """
        Reprojects a given dataset to a target CRS.
        :return: (GDALDatasetShadow) gdal dataset object reprojected to output CRS.
        """
        # TODO
        return None
    
    @staticmethod
    def reprojectCoordinates(coordinates, inputCrs, outputCrs):
        """
        Reproject a tuple of coordinates (y, x[, z]) to output CRS.
        :param coordinates: (tuple-of-float) coordinates to be reprojected in the shape (y, x[, z]).
        :param inputCrs: (int) auth ID for input CRS.
        :param outputCrs: (int) auth ID for output CRS.
        :return: (tuple-of-float) reprojected coordinates.
        """
        # TODO
        return (None, None) if len(coordinates) == 2 else (None, None, coordinates[2])
