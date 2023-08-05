"""
`stemma_soil`
================================================================================

Python library for Hydros21 or Decagon CDT-10 water level sensor.

**Author(s):** `Colby Sawyer <https://github.com/ColbySawyer7>`_

Implementation Notes
--------------------
**Hardware:**
* `Stemma Soil Sensor `_

**Software and Dependencies:**

"""

import time
import board
from adafruit_seesaw.seesaw import Seesaw
import logging
from esdn_sensing.sensor_error import SensorError

def sensor_run():
    """Runs the sensor specific operations and collects/summarizes the data.

    Returns:
        [int]: [Returns array of integers mapped to the corresponding values ([temperature, moisture])]
    """
    i2c_bus = board.I2C()
    ss = Seesaw(i2c_bus, addr=0x36)
    # read moisture level through capacitive touch pad
    touch = ss.moisture_read()
    # read temperature from the temperature sensor
    temp = ss.get_temp()

    logging.debug("temp: " + str(temp) + "  moisture: " + str(touch))
    return [temp, touch]

class StemmaSoil:
    """Driver class for Stemma Soil Moisture sensor
    """
    temperature = 0
    moisture = 0

    def init(self, temperature=0, moisture=0):
        """Initialize instance of sensor

        Args:
            temperature (int, optional): Temperature (Celcius). Defaults to 0.
            moisture (int, optional): Moisture. Defaults to 0.
        """
        self.temperature = temperature
        self.moisture = moisture

    def get_data(self, dec_factor=100):
        """Collects data from the device attached via the sensor_run method

        Args:
            dec_factor (int, optional): [Holds the decimal factor to be used for integer conversion]. Defaults to 100.

        Returns:
           [Bytearray]: [Packaged up data to be sent via LoRa driving code]
        """
        try:
            sensor_readings = sensor_run()

            self.temperature = sensor_readings[0]
            self.moisture = sensor_readings[1] 


            temperature= int((self.temperature*dec_factor))
            logging.debug("temperature: %0.1f %%" % temperature)

            moisture= int((self.moisture*dec_factor))
            logging.debug("moisture %0.1f %%" % moisture)

            sensor_data = bytearray(4)

            sensor_data[0] = (temperature >> 8) & 0xff
            sensor_data[1]= temperature & 0xff
            
            sensor_data[2] = (moisture >> 8) & 0xff
            sensor_data[3] = moisture & 0xff

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

                self.temperature = sensor_readings[0]
                self.moisture = sensor_readings[1] 


                temperature= int((self.temperature*dec_factor))
                print("temperature: %0.1f %%" % temperature)

                moisture= int((self.moisture*dec_factor))
                print("moisture %0.1f %%" % moisture)

            except:
                raise SensorError('Unable to connect')

