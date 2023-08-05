"""
`aht20`
================================================================================

*Python library for AHT20 Environmental Sensor*

**Author(s):** `Colby Sawyer <https://github.com/ColbySawyer7>`_

Implementation Notes
--------------------
**Hardware:**
`aht20 `_

**Software and Dependencies:**
Utilizing circuit python library based on work from `Adafruit`_
"""

from time import sleep
import logging
from esdn_sensing.sensor_error import SensorError
import adafruit_ahtx0
import board

def sensor_run():
    """Runs the sensor specific operations and collects/summarizes the data.

    Returns:
        [int]: [Returns array of integers mapped to the corresponding values ([temperature, humidity])]
    """
    # Create sensor object, using the board's default I2C bus.
    i2c = board.I2C()   # uses board.SCL and board.SDA
    aht20 = adafruit_ahtx0.AHTx0(i2c)


    # Get sensor readings
    temp_val = int(aht20.temperature)
    logging.debug("\nTemperature: %0.1f C" % temp_val)
    humid_val = int(aht20.relative_humidity)
    logging.debug("Humidity: %0.1f %%" % humid_val)

    return [temp_val, humid_val]

class AHT20:
    """Driver class for AHT20 Environmental Sensor
    """
    temperature = 0
    humidity = 0

    def init(self, temperature=0, humidity=0):
        """Initialize instance of sensor

        Args:
            temperature (int, optional): Temperature (Celcius). Defaults to 0.
            humidity (int, optional): Humidity. Defaults to 0.
        """
        self.temperature = temperature
        self.humidity = humidity

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
            self.humidity = sensor_readings[1] 

            sensor_data = bytearray(4)
            # Temperature data
            sensor_data[0] = (self.temperature >> 8) & 0xff
            sensor_data[1] = self.temperature & 0xff
            # Humidity data
            sensor_data[2] = (self.humidity >> 8) & 0xff
            sensor_data[3] = self.humidity & 0xff


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
                self.humidity = sensor_readings[1] 

                temperature= int((self.temperature*dec_factor))
                print("visible_light: %0.1f %%" % temperature)

                humidity= int((self.humidity*dec_factor))
                print("humidity %0.1f %%" % humidity)


            except:
                raise SensorError('Unable to connect')
