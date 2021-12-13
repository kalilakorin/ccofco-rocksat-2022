'''
    This file hanles the polling and recording of sensor data.
    Contributors:
	    Jillian Frimml
	    Skyler Puckett
        Konstantin Zaremski
'''

# Import modules
from time import sleep
import time
import logging

import board
import busio
import adafruit_mpl115a2

# Acquire the existing logger
try:
    logger = logging.getLogger(__name__)
except:
    logger = None
    print('Unable to acquire the global logger object, assuming that sensors.py is being run on its own')

# Main sensor program loop
def main():
    # Configure & initialize the sensors
    logging.info('Initializing sensors')

    # Begin i2c
    try:
        i2c = busio.I2C(board.SCL, board.SDA)
        logging.info('I2C interface ... OK')
    except: 
        logging.error('Failed to enable i2c interface')

    # Begin mpl
    try:
        mpl = adafruit_mpl115a2.MPL115A2(i2c)
        logging.info('MPL115A2 (temperature, pressure) ... OK')
    except: 
        logging.error('Failed to enable MPL115A2 sensor')

    logging.info('Sensors initialized')

    # Start the sensor output file
    datafileName = './data-sensors/sensors-' + str(int(time.time() * 1000)) + '.csv'
    datafile = open(datafileName, 'w') 
    logging.info('Opened sensor data file for writing: ' + datafileName)

    # Sensor sample and data write loop
    logging.info('Beginning sensor polling and writing (1000 samples/second)')
    while True:
        csvline = f'{str(int(time.time() * 1000))},{str(mpl.pressure)},{str(mpl.temperature)}'
        datafile.write(csvline + '\n')
        if logger == None: print(csvline)
        sleep(0.001)

if __name__ == '__main__':
    main()