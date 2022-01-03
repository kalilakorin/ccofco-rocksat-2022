'''
    This file handles the polling and recording of sensor data.
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
from adafruit_bme280 import basic as adafruit_bme280
import VL53L1X

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
        logging.critical('Failed to enable i2c interface, the sensor thread will now crash')
        return
    # Init mpl sensor
    try:
        mpl115a2 = adafruit_mpl115a2.MPL115A2(i2c)
        logging.info('MPL115A2 (temperature, pressure) ... OK')
    except: 
        mpl115a2 = None
        logging.error('Failed to enable MPL115A2 sensor')
    # Init bme280
    try:
        bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
    except:
        bme280 = None
        logging.error('Failed to enable BME280 (temperature, pressure, humidity) sensor')
    # Init vl53l1x distance sensor
    try:
        vl53l1x = VL53l1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
        vl53l1x.open()
        vl53l1x.start_ranging(1)
    except:
        vl53l1x = None
        logging.error('Failed to enable VL53L1X (distance) sensor')

    logging.info('Sensors initialized')

    # Start the sensor output file
    datafileName = './data-sensors/sensors-' + str(int(time.time() * 1000)) + '.csv'
    datafile = open(datafileName, 'w') 
    logging.info('Opened sensor data file for writing: ' + datafileName)

    # CSV header line
    csvheader = 'Time'
    if mpl115a2 != None: csvheader += ',MPL115A2 Temperature, MPL115A2 Pressure'
    if bme280 != None: csvheader += ',BME280 Temperature, BME280 Pressure, BME280 Humidity'
    if vl53l1x != None: csvheader += ',vl53l1x Distance'
    datafile.write(csvheader + '\n')
    logging.info(f'Sensor file CSV columns are as follows: {csvheader}')

    # Sensor sample and data write loop
    logging.info('Beginning sensor polling and writing (1000 samples/second)')
    while True:
        # Time axis
        csvline = str(int(time.time() * 1000))
        
        # Add entries to the CSV line based on the presence of those particular sensors
        if mpl115a2 != None: csvline += f',{mpl115a2.temperature},{mpl115a2.pressure}'
        if bme280 != None: csvline += f',{bme280.temperature},{bme280.pressure},{bme280.relative_humidity}'
        if vl53l1x != None: csvline += f',{vl53l1x.get_distance()}'
        
        datafile.write(csvline + '\n')
        # Print the CSV line to the console if the file is running standalone
        if logger == None: print(csvline)
        sleep(0.001)

if __name__ == '__main__':
    main()
