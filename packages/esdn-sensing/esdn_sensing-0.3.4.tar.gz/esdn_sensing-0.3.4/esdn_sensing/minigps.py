"""
`minigps`
================================================================================

*Python library for LTR-390 Visible Light Sensor*

**Author(s):** `Colby Sawyer <https://github.com/ColbySawyer7>`_

Implementation Notes
--------------------
**Hardware:**
`Mini GPS <https://www.adafruit.com/product/5610>`_

**Software and Dependencies:**
Utilizing circuit python library based on work from `Adafruit <https://github.com/adafruit/Adafruit_CircuitPython_GPS>`_
"""

from time import sleep
import logging
from esdn_sensing.sensor_error import SensorError
import adafruit_gps

def sensor_run():
    """Runs the sensor specific operations and collects/summarizes the data.

    Returns:
        [int]: [Returns array of integers mapped to the corresponding values ([longitude_degrees, longitude_minutes, latitude_degrees, latitude_minutes, satellites])]
    """
    i2c = board.I2C()  # uses board.SCL and board.SDA
    gps = adafruit_gps.GPS_GtopI2C(i2c, debug=False)  # Use I2C interface

    # Turn on the basic GGA and RMC info (what you typically want)
    gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

    # Set update rate to once a second (1hz) which is what you typically want.
    gps.send_command(b"PMTK220,1000")

    gps.update()

    long_deg = gps.longitude_degrees
    long_min = gps.longitude_minutes
    lat_deg = gps.latitude_degrees
    lat_min = gps.latitude_minutes
    satellites = gps.satellites


    logging.debug("Longitude Degrees:", long_deg)
    logging.debug("Longitude Minutes:", long_min)
    logging.debug("Latitude Degrees:", lat_deg)
    logging.debug("Latitude Minutes:", lat_min)
    logging.debug("Current Satellites:", satellites)


    return [long_deg, long_min, lat_deg, lat_min, satellites]

class MiniGPS:
    """Driver class for MiniGPS sensor
    """
    long_deg = 0
    long_min = 0
    lat_deg = 0
    lat_min = 0
    satellites = 0

    def init(self,long_deg=0, long_min=0, lat_deg=0, lat_min=0, satellites=0):
        """Initialize instance of sensor

        Args:
            long_deg (int, optional): Longitude Degrees. Defaults to 0.
            long_min (int, optional): Longitude Minutes. Defaults to 0.
            lat_def (int, optional): Latitude Degrees. Defaults to 0.
            lat_min (int, optional): Latitude Minutes. Defaults to 0.
            satellites (int, optional): Available Satellites count. Defaults to 0.
        """
        self.long_deg = long_deg
        self.long_min = long_min
        self.lat_deg = lat_deg
        self.lat_min = lat_min
        self.satellites = satellites

    def get_data(self, dec_factor=100):
        """Collects data from the device attached via the sensor_run method

        Args:
            dec_factor (int, optional): [Holds the decimal factor to be used for integer conversion]. Defaults to 100.

        Returns:
           [Bytearray]: [Packaged up data to be sent via LoRa driving code]
        """
        try:
            sensor_readings = sensor_run()

            self.long_deg = sensor_readings[0]
            self.long_min = sensor_readings[1]
            self.lat_deg = sensor_readings[2]
            self.lat_min = sensor_readings[3]
            self.satellites = sensor_readings[4]

            long_deg= int((self.long_deg*dec_factor))
            logging.debug("long_deg: %0.1f %%" % long_deg)

            long_min= int((self.long_min*dec_factor))
            logging.debug("long_min %0.1f %%" % long_min)

            lat_deg= int((self.lat_deg*dec_factor))
            logging.debug("lat_deg %0.1f %%" % lat_deg)

            lat_min= int((self.lat_min*dec_factor))
            logging.debug("lat_min %0.1f %%" % lat_min)

            satellites = int((self.satellites*dec_factor))
            logging.debug("satellites %0.1f %%" % satellites)

            sensor_data = bytearray(10)

            sensor_data[0] = (long_deg >> 8) & 0xff
            sensor_data[1]= long_deg & 0xff
            
            sensor_data[2] = (long_min >> 8) & 0xff
            sensor_data[3] = long_min & 0xff

            sensor_data[4] = (lat_deg >> 8) & 0xff
            sensor_data[5] = lat_deg & 0xff

            sensor_data[6] = (lat_min >> 8) & 0xff
            sensor_data[7] = lat_min & 0xff

            sensor_data[8] = (satellites >> 8) & 0xff
            sensor_data[9] = satellites & 0xff

            return sensor_data

        except:
            raise SensorError('Unable to connect')

    def test(self,dec_factor=100):
            """Test that the device is connected and prints sample data

            Args:
                dec_factor (int, optional): [Holds the decimal factor to be used for integer conversion]. Defaults to 100.

            """
            try:
                sensor_readings = sensor_run()

                self.long_deg = sensor_readings[0]
                self.long_min = sensor_readings[1]
                self.lat_deg = sensor_readings[2]
                self.lat_min = sensor_readings[3]
                self.satellites = sensor_readings[4]

                long_deg= int((self.long_deg*dec_factor))
                print("long_deg: %0.1f %%" % long_deg)

                long_min= int((self.long_min*dec_factor))
                print("long_min %0.1f %%" % long_min)

                lat_deg= int((self.lat_deg*dec_factor))
                print("lat_deg %0.1f %%" % lat_deg)

                lat_min= int((self.lat_min*dec_factor))
                print("lat_min %0.1f %%" % lat_min)

                satellites = int((self.satellites*dec_factor))
                print("satellites %0.1f %%" % satellites)

            except:
                raise SensorError('Unable to connect')
