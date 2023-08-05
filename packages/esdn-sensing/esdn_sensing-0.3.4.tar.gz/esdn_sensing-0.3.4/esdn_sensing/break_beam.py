"""
`break_beam`
================================================================================

*Python library for LTR-390 Visible Light Sensor*

**Author(s):** `Colby Sawyer <https://github.com/ColbySawyer7>`_

Implementation Notes
--------------------
**Hardware:**
`Break Beam <https://www.adafruit.com/product/2167>`_

**Software and Dependencies:**

"""

from time import sleep
import logging
from esdn_sensing.sensor_error import SensorError
import board
import digitalio

def sensor_run(sample_size):
    """Runs the sensor specific operations and collects/summarizes the data.

    Args:
        sample_size (int, mandatory): Sample size (seconds) of sample window

    Returns:
        [int]: [Returns array of integers mapped to the corresponding values ([broken, total_breaks)]
    """
    break_beam = digitalio.DigitalInOut(board.D23)
    break_beam.direction = digitalio.Direction.INPUT
    break_beam.pull = digitalio.Pull.UP     

    total_breaks = 0
    broken = False

    logging.debug("Starting sample window.... \nListening to beam")
    for x in range(sample_size):
        if not break_beam.value:
            logging.debug("Beam is broken")
            total_breaks += 1
            broken = True
        # Delay for one second to enforce timing window 
        time.sleep(1.0) 

    logging.debug("Sample window closed")

    return [broken, total_breaks]

class BreakBeam:
    """Driver class for LTR 390 Light Sensor
    """
    broken = False
    total_breaks = 0

    def init(self,broken=False, total_breaks=0):
        """Initialize instance of sensor

        Args:
            uv (int, optional): Calculated UV value. Defaults to 0.
            ambient_light (int, optional): Measure ambient light level. Defaults to 0.
            uvi (int, optional): UV Index, based upon the rated sensitivity, of 1 UVI per 2300 counts at 18x gain factor and 20 bit-resolution (default). Defaults to 0.
            lux (int, optional): Calculated light value. Defaults to 0.
        """
        self.broken = broken
        self.total_breaks = total_breaks

    def get_data(self, sample_size = 10, dec_factor=100):
        """Collects data from the device attached via the sensor_run method

        Args:
            sample_size (int, mandatory): [Sample size (seconds) of collection]
            dec_factor (int, optional): [Holds the decimal factor to be used for integer conversion]. Defaults to 100.

        Returns:
           [Bytearray]: [Packaged up data to be sent via LoRa driving code]
        """
        try:
            sensor_readings = sensor_run(sample_size)

            self.broken = sensor_readings[0]
            self.total_breaks = sensor_readings[1]

            broken = int((self.broken))
            logging.debug("Broken (integer): %0.1f %%" % broken)

            total_breaks = int((self.total_breaks*dec_factor))
            logging.debug("total breaks:  %0.1f %%" % total_breaks)

            sensor_data = bytearray(4)

            sensor_data[0] = (broken >> 8) & 0xff
            sensor_data[1]= broken & 0xff
            
            sensor_data[2] = (total_breaks >> 8) & 0xff
            sensor_data[3] = total_breaks & 0xff

            return sensor_data

        except:
            raise SensorError('Unable to connect')

    def test(self, sample_size=10,dec_factor=1):
            """Test that the device is connected and prints sample data

            Args:
                sample_size (int, mandatory): [Sample size (seconds) of collection]
                dec_factor (int, optional): [Holds the decimal factor to be used for integer conversion]. Defaults to 1.

            """
            try:
                sensor_readings = sensor_run(sample_size)

                self.broken = sensor_readings[0]
                self.total_breaks = sensor_readings[1]

                broken = int((self.broken))
                print("Broken (integer): %0.1f %%" % broken)

                total_breaks = int((self.total_breaks*dec_factor))
                print("total breaks:  %0.1f %%" % total_breaks)
            except:
                raise SensorError('Unable to connect')
