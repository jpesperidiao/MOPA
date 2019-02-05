from Core.Sensor.sensorsManager import SensorsManager
from Core.Observation.observationsManager import ObservationsManager
from Settings.settings import Settings
from Core.ProcessingTools.rasterLayer import RasterLayer
from Core.ProcessingTools.shooterFinder import ShooterFinder
import numpy as np
from Core.enums import Enums

def generateObsAtPixel(dem, sensor, col, lin):
       """
       Generates an observations at a given column / line of a raster.
       :param col: (int) shooter's column.
       :param lin: (int) shooter's line.
       :return: (Observation) observation at col, pix.
       """
       # handle outside points - put them back to the borders
       if col > dem.width():
              col = dem.width() - 1
       elif col < 0:
              col = 0
       if lin > dem.height():
              lin = dem.height() - 1
       elif lin < 0:
              lin = 0
       y, x = dem.pixelToCoordinates(col, lin)
       z = dem.bands()[col][lin]
       sensorY, sensorX, sensorZ = sensor['coordinates']
       dx, dy, dz = x - sensorX, y - sensorY, z - sensorZ
       if dem.isGeographic():
              # the more appropriate conversion would be a geodesic line - curve geometry
              dx = np.deg2rad(dx) * Enums.EARTH_RADIUS
              dy = np.deg2rad(dy) * np.pi * Enums.EARTH_RADIUS / 180
       azimuth = np.rad2deg(np.arctan2(np.sqrt(dy ** 2 + dz ** 2), dx))
       zenith = np.rad2deg(np.arctan2(dx, dz))
       om = ObservationsManager()
       om.addObservation(azimuth, zenith, sensor['id'])
       return zenith, azimuth

s = Settings()
sm = SensorsManager(s)
sensor = sm.getSensorFromId(3)
om = ObservationsManager(s)

demPath = ".dev/testing_data/sf-23-z-b/rj_srtm_90m_sirgas2000-23s.tif"
dem = RasterLayer(demPath)
generateObsAtPixel(dem, sensor, 102, 101)
obs = om.getObservationsFromSensor(3)[17]
sf = ShooterFinder(s)
sf.findShooter(1, sensor, obs, dem)
print(om.getObservationsFromSensor(3))
