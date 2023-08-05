"""
`ltr390`
================================================================================

*Python library for LTR-390 Visible Light Sensor*

**Author(s):** `Colby Sawyer <https://github.com/ColbySawyer7>`_

Implementation Notes
--------------------
**Hardware:**
`LTR-390 <https://www.adafruit.com/product/5610>`_

**Software and Dependencies:**
Utilizing circuit python library based on work from `Adafruit <https://github.com/adafruit/Adafruit_CircuitPython_LTR390>`_
"""

from time import sleep
import logging
from esdn_sensing.sensor_error import SensorError
import adafruit_ltr390

def sensor_run():
    """Runs the sensor specific operations and collects/summarizes the data.

    Returns:
        [int]: [Returns array of integers mapped to the corresponding values ([uv, ambient_light, uvi, lux])]
    """
    i2c = board.I2C()  # uses board.SCL and board.SDA
    time.sleep(0.1)  # sensor takes 100ms to 'boot' on power up
    ltr390 = LTR390(i2c)

    uv = ltr390.uvs
    ambient_light = ltr390.light
    uvi = ltr390.uvi
    lux = ltr390.lux

    logging.debug("UV:", ltr.uvs, "\t\tAmbient Light:", ltr.light)
    logging.debug("UVI:", ltr.uvi, "\t\tLux:", ltr.lux)

    return [uv, ambient_light, uvi, lux]

class LTR390:
    """Driver class for LTR 390 Light Sensor
    """
    uv = 0
    ambient_light = 0
    uvi = 0
    lux = 0

    def init(self,uv=0,ambient_light=0, uvi=0,lux=0):
        """Initialize instance of sensor

        Args:
            uv (int, optional): Calculated UV value. Defaults to 0.
            ambient_light (int, optional): Measure ambient light level. Defaults to 0.
            uvi (int, optional): UV Index, based upon the rated sensitivity, of 1 UVI per 2300 counts at 18x gain factor and 20 bit-resolution (default). Defaults to 0.
            lux (int, optional): Calculated light value. Defaults to 0.
        """
        self.uv = uv
        self.ambient_light = ambient_light
        self.uvi = uvi
        self.lux = lux

    def get_data(self, dec_factor=100):
        """Collects data from the device attached via the sensor_run method

        Args:
            dec_factor (int, optional): [Holds the decimal factor to be used for integer conversion]. Defaults to 100.

        Returns:
           [Bytearray]: [Packaged up data to be sent via LoRa driving code]
        """
        try:
            sensor_readings = sensor_run()

            self.uv = sensor_readings[0]
            self.ambient_light = sensor_readings[1]
            self.uvi = sensor_readings[2]
            self.lux = sensor_readings[3]

            uv= int((self.uv*dec_factor))
            logging.debug("uv: %0.1f %%" % uv)

            ambient_light= int((self.ambient_light*dec_factor))
            logging.debug("ambient_light %0.1f %%" % ambient_light)

            uvi= int((self.uvi*dec_factor))
            logging.debug("uvi %0.1f %%" % uvi)

            lux= int((self.lux*dec_factor))
            logging.debug("lux %0.1f %%" % lux)

            sensor_data = bytearray(8)

            sensor_data[0] = (uv >> 8) & 0xff
            sensor_data[1]= uv & 0xff
            
            sensor_data[2] = (ambient_light >> 8) & 0xff
            sensor_data[3] = ambient_light & 0xff

            sensor_data[4] = (uvi >> 8) & 0xff
            sensor_data[5] = uvi & 0xff

            sensor_data[6] = (lux >> 8) & 0xff
            sensor_data[7] = lux & 0xff

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

                self.uv = sensor_readings[0]
                self.ambient_light = sensor_readings[1]
                self.uvi = sensor_readings[2]
                self.lux = sensor_readings[3]

                uv= int((self.uv*dec_factor))
                print("uv: %0.1f %%" % uv)

                ambient_light= int((self.ambient_light*dec_factor))
                print("ambient_light %0.1f %%" % ambient_light)

                uvi= int((self.uvi*dec_factor))
                print("uvi %0.1f %%" % uvi)

                lux= int((self.lux*dec_factor))
                print("lux %0.1f %%" % lux)

            except:
                raise SensorError('Unable to connect')
