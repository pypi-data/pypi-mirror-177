"""
`bme280`
================================================================================

*Python library for BME280 Environmental Sensor*

**Author(s):** `Colby Sawyer <https://github.com/ColbySawyer7>`_

Implementation Notes
--------------------
**Hardware:**
`BME280 `_

**Software and Dependencies:**
Utilizing circuit python library based on work from `Adafruit`_
"""

from time import sleep
import logging
from esdn_sensing.sensor_error import SensorError
from adafruit_bme280 import basic as adafruit_bme280
import board

def sensor_run():
    """Runs the sensor specific operations and collects/summarizes the data.

    Returns:
        [int]: [Returns array of integers mapped to the corresponding values ([temperature, humidity, pressure])]
    """
    # Create sensor object, using the board's default I2C bus.
    i2c = board.I2C()   # uses board.SCL and board.SDA
    bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

    # change this to match the location's pressure (hPa) at sea level
    bme280.sea_level_pressure = 1013.2

    # Get sensor readings
    temp_val = int(bme280.temperature)
    logging.debug("\nTemperature: %0.1f C" % temp_val)
    humid_val = int(bme280.humidity)
    logging.debug("Humidity: %0.1f %%" % humid_val)
    press_val = int(bme280.pressure)
    logging.debug("Pressure: %0.1f hPa" % press_val)

    return [temp_val, humid_val, press_val]

class BME280:
    """Driver class for BME280 Environmental Sensor
    """
    temperature = 0
    humidity = 0
    pressure = 0

    def init(self, temperature=0, humidity=0,pressure=0):
        """Initialize instance of sensor

        Args:
            temperature (int, optional): Temperature (Celcius). Defaults to 0.
            humidity (int, optional): Humidity. Defaults to 0.
            pressure (int, optional): Atmospheric Pressure. Defaults to 0.
        """
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure

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
            self.pressure = sensor_readings[2]

            sensor_data = bytearray(6)
            # Temperature data
            sensor_data[0] = (self.temperature >> 8) & 0xff
            sensor_data[1] = self.temperature & 0xff
            # Humidity data
            sensor_data[2] = (self.humidity >> 8) & 0xff
            sensor_data[3] = self.humidity & 0xff
            #Pressure Data
            sensor_data[4] = (self.pressure >> 8) & 0xff
            sensor_data[5] = self.pressure & 0xff

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
                self.pressure = sensor_readings[2]


                temperature= int((self.temperature*dec_factor))
                print("visible_light: %0.1f %%" % temperature)

                humidity= int((self.humidity*dec_factor))
                print("humidity %0.1f %%" % humidity)

                pressure= int((self.pressure*dec_factor))
                print("humidity %0.1f %%" % pressure)


            except:
                raise SensorError('Unable to connect')
