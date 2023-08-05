"""
`us100`
================================================================================

*Python library for US-100 Ultrasonic Distance Sensor*

**Author(s):** `Colby Sawyer <https://github.com/ColbySawyer7>`_

Implementation Notes
--------------------
**Hardware:**
`US-100 <https://www.adafruit.com/product/4019>`_

**Software and Dependencies:**
Utilizing circuit python library based on work from `Adafruit <https://github.com/adafruit/Adafruit_CircuitPython_US100>`_
"""

from time import sleep
import logging
from esdn_sensing.sensor_error import SensorError
import adafruit_us100

def sensor_run():
    """Runs the sensor specific operations and collects/summarizes the data.

    Returns:
        [int]: [Returns array of integers mapped to the corresponding values ([distance, temperature])]
    """
    uart = busio.UART(board.TX, board.RX, baudrate=9600)
    # Create a US-100 module instance.
    us100 = adafruit_us100.US100(uart)

    distance = us100.distance
    temp = us100.temperature

    logging.debug("Distance:", distance, "\t\tTemperature:", temp)

    return [distance, temp]

class US100:
    """Driver class for US-100 Distance Detection Sensor
    """
    distance  = 0
    temperature = 0

    def init(self,distance=0, temperature=0):
        """Initialize instance of sensor

        Args:
            distance (int, optional): Distance measured(mm). Defaults to 0.
            temperature (int, optional): Temperature. Defaults to 0.

        """
        self.distance = distance
        self.temperature = temperature

    def get_data(self, dec_factor=100):
        """Collects data from the device attached via the sensor_run method

        Args:
            dec_factor (int, optional): [Holds the decimal factor to be used for integer conversion]. Defaults to 100.

        Returns:
           [Bytearray]: [Packaged up data to be sent via LoRa driving code]
        """
        try:
            sensor_readings = sensor_run()

            self.distance = sensor_readings[0]
            self.temperature = sensor_readings[1]


            distance= int((self.distance*dec_factor))
            logging.debug("distance: %0.1f %%" % distance)

            temperature= int((self.temperature*dec_factor))
            logging.debug("temperature %0.1f %%" % temperature)

            sensor_data = bytearray(4)

            sensor_data[0] = (distance >> 8) & 0xff
            sensor_data[1]= distance & 0xff
            
            sensor_data[2] = (temperature >> 8) & 0xff
            sensor_data[3] = temperature & 0xff

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

                self.distance = sensor_readings[0]
                self.temperature = sensor_readings[1]


                distance= int((self.distance*dec_factor))
                print("distance: %0.1f %%" % distance)

                temperature= int((self.temperature*dec_factor))
                print("temperature %0.1f %%" % temperature)
            except:
                raise SensorError('Unable to connect')
