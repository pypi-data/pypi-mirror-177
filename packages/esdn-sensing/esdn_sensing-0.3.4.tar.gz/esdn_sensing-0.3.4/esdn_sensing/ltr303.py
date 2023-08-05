"""
`ltr303`
================================================================================

*Python library for LTR-303 Visible Light Sensor*

**Author(s):** `Colby Sawyer <https://github.com/ColbySawyer7>`_

Implementation Notes
--------------------
**Hardware:**
`LTR-303 <https://www.adafruit.com/product/5610>`_

**Software and Dependencies:**
Utilizing circuit python library based on work from `Adafruit <https://github.com/adafruit/Adafruit_CircuitPython_LTR329_LTR303/blob/main`_
"""

from time import sleep
import logging
from esdn_sensing.sensor_error import SensorError
from adafruit_ltr329_ltr303 import LTR303


def sensor_run():
    """Runs the sensor specific operations and collects/summarizes the data.

    Returns:
        [int]: [Returns array of integers mapped to the corresponding values ([visible_light, infrared_light])]
    """
    i2c = board.I2C()  # uses board.SCL and board.SDA
    time.sleep(0.1)  # sensor takes 100ms to 'boot' on power up
    ltr303 = LTR303(i2c)

    visible = ltr303.visible_plus_ir_light
    infrared = ltr303.ir_light

    logging.debug("Visible + IR:", visible)
    logging.debug("Infrared    :", infrared)

    return [visible, infrared]

class LTR303:
    """Driver class for LTR Light Sensor
    """
    visible_light = 0
    infrared_light = 0

    def init(self, visible_light=0, infrared_light=0):
        """Initialize instance of sensor

        Args:
            visible_light (int, optional): Visible Light plus Infrared. Defaults to 0.
            infrared_light (int, optional): Infrared light. Defaults to 0.
        """
        self.visible_light = visible_light
        self.infrared_light = infrared_light

    def get_data(self, dec_factor=100):
        """Collects data from the device attached via the sensor_run method

        Args:
            dec_factor (int, optional): [Holds the decimal factor to be used for integer conversion]. Defaults to 100.

        Returns:
           [Bytearray]: [Packaged up data to be sent via LoRa driving code]
        """
        try:
            sensor_readings = sensor_run()

            self.visible_light = sensor_readings[0]
            self.infrared_light = sensor_readings[1] 


            visible_light= int((self.visible_light*dec_factor))
            logging.debug("visible_light: %0.1f %%" % visible_light)

            infrared_light= int((self.infrared_light*dec_factor))
            logging.debug("infrared_light %0.1f %%" % infrared_light)

            sensor_data = bytearray(4)

            sensor_data[0] = (visible_light >> 8) & 0xff
            sensor_data[1]= visible_light & 0xff
            
            sensor_data[2] = (infrared_light >> 8) & 0xff
            sensor_data[3] = infrared_light & 0xff

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

                self.visible_light = sensor_readings[0]
                self.infrared_light = sensor_readings[1] 


                visible_light= int((self.visible_light*dec_factor))
                print("visible_light: %0.1f %%" % visible_light)

                infrared_light= int((self.infrared_light*dec_factor))
                print("infrared_light %0.1f %%" % infrared_light)

            except:
                raise SensorError('Unable to connect')
