"""
`vl680x`
================================================================================

*Python library for VL6180x Time of Flight Distance Ranging Sensor*

**Author(s):** `Colby Sawyer <https://github.com/ColbySawyer7>`_

Implementation Notes
--------------------
**Hardware:**
`Vl6180x ToF <https://www.adafruit.com/product/3316>`_

**Software and Dependencies:**
Utilizing circuit python library based on work from `Adafruit <https://github.com/adafruit/Adafruit_CircuitPython_VL6180X>`_
"""

from time import sleep
import logging
from esdn_sensing.sensor_error import SensorError
import adafruit_vl6180x

def sensor_run(sample_size):
    """Runs the sensor specific operations and collects/summarizes the data.

    Args:
        sample_size (int, mandatory): The number of seconds that the sensor will sample


    Returns:
        [int]: [Returns array of integers mapped to the corresponding values ([range_min, range_max, range_avg, lux_min, lux_max, lux_avg])]
    """
    # Create I2C bus.
    i2c = busio.I2C(board.SCL, board.SDA)
    # Create sensor instance.
    sensor = adafruit_vl6180x.VL6180X(i2c)

    range_sample = [sample_size]
    lux_sample =[sample_size]

    for i in range(sample_size):
            # Grab the latest data
            range_sample[i] = sensor.range
            logging.debug('Range (mm):' + str(range_sample[i]))
            lux_sample[i] = sensor.read_lux(adafruit_vl6180x.ALS_GAIN_1)
            logging.debug('Lux: ' + str(lux_sample[i]))

            #Force to adhere to 1 second per loop
            sleep(1)

    # Process Data post sample window        
    range_min = min(range_sample)
    range_max = max(range_sample)
    range_avg = sum(range_sample)/len(range_sample)

    lux_min = min(lux_sample)
    lux_max = max(lux_sample)
    lux_avg = sum(lux_sample)/len(lux_sample)

    return [range_min, range_max, range_avg, lux_min, lux_max, lux_avg]

class VL6180x:
    """Driver class for VL6180X Time of Flight Distance Ranging Sensor
    """
    range_min = 0
    range_max = 0
    range_avg = 0
    lux_min = 0
    lux_max = 0
    lux_avg = 0

    def init(self,range_min=0, range_max=0, range_avg=0,lux_min=0,lux_max=0, lux_avg= 0):
        """Initialize instance of sensor

        Args:
            range_min (int, optional): Range (mm) minimum during sample window. Defaults to 0.
            range_max (int, optional): Range (mm) maximum during sample window. Defaults to 0.
            range_avg (int, optional): Range (mm) average during sample window. Defaults to 0.
            lux_min (int, optional): Lux minimum during sample window. Defaults to 0.
            lux_max (int, optional): Lux maximum during sample window. Defaults to 0.
            lux_avg (int, optional): Lux average during sample window. Defaults to 0.

        """
        self.range_min = range_min
        self.range_max = range_max
        self.range_avg = range_avg
        self.lux_min = lux_min
        self.lux_max = lux_max
        self.lux_avg = lux_avg


    def get_data(self, sample_size = 10, dec_factor=100):
        """Collects data from the device attached via the sensor_run method

        Args:
            dec_factor (int, optional): [Holds the decimal factor to be used for integer conversion]. Defaults to 100.

        Returns:
           [Bytearray]: [Packaged up data to be sent via LoRa driving code]
        """
        try:
            sensor_readings = sensor_run(sample_size)

            self.range_min = sensor_readings[0]
            self.range_max = sensor_readings[1]
            self.range_avg = sensor_readings[2]
            self.lux_min = sensor_readings[3]
            self.lux_max = sensor_readings[4]
            self.lux_avg = sensor_readings[5]

            range_min= int((self.range_min*dec_factor))
            logging.debug("range_min: %0.1f %%" % range_min)

            range_max= int((self.range_max*dec_factor))
            logging.debug("range_max %0.1f %%" % range_max)

            range_avg= int((self.range_avg*dec_factor))
            logging.debug("range_avg %0.1f %%" % range_avg)

            lux_min= int((self.lux_min*dec_factor))
            logging.debug("lux_min %0.1f %%" % lux_min)

            lux_max= int((self.lux_max*dec_factor))
            logging.debug("lux_max %0.1f %%" % lux_max)

            lux_avg= int((self.lux_avg*dec_factor))
            logging.debug("lux_avg %0.1f %%" % lux_avg)

            sensor_data = bytearray(12)

            sensor_data[0] = (range_min >> 8) & 0xff
            sensor_data[1]= range_min & 0xff
            
            sensor_data[2] = (range_max >> 8) & 0xff
            sensor_data[3] = range_max & 0xff

            sensor_data[4] = (range_avg >> 8) & 0xff
            sensor_data[5] = range_avg & 0xff

            sensor_data[6] = (lux_min >> 8) & 0xff
            sensor_data[7] = lux_min & 0xff

            sensor_data[8] = (lux_max >> 8) & 0xff
            sensor_data[9] = lux_max & 0xff

            sensor_data[10] = (lux_avg >> 8) & 0xff
            sensor_data[11] = lux_avg & 0xff

            return sensor_data

        except:
            raise SensorError('Unable to connect')

    def test(self, sample_size=10, dec_factor=100):
            """Test that the device is connected and prints sample data

            Args:
                dec_factor (int, optional): [Holds the decimal factor to be used for integer conversion]. Defaults to 100.

            """
            try:
                sensor_readings = sensor_run(sample_size)

                self.range_min = sensor_readings[0]
                self.range_max = sensor_readings[1]
                self.range_avg = sensor_readings[2]
                self.lux_min = sensor_readings[3]
                self.lux_max = sensor_readings[4]
                self.lux_avg = sensor_readings[5]

                range_min= int((self.range_min*dec_factor))
                print("range_min: %0.1f %%" % range_min)

                range_max= int((self.range_max*dec_factor))
                print("range_max %0.1f %%" % range_max)

                range_avg= int((self.range_avg*dec_factor))
                print("range_avg %0.1f %%" % range_avg)

                lux_min= int((self.lux_min*dec_factor))
                print("lux_min %0.1f %%" % lux_min)

                lux_max= int((self.lux_max*dec_factor))
                print("lux_max %0.1f %%" % lux_max)

                lux_avg= int((self.lux_avg*dec_factor))
                print("lux_avg %0.1f %%" % lux_avg)

            except:
                raise SensorError('Unable to connect')
