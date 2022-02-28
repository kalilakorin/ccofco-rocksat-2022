'''
    This file handles the polling and recording of sensor data.
    Contributors:
        Jillian Frimml
        Skyler Puckett
        Konstantin Zaremski
'''

# Import system modules
from time import sleep
import time
import logging
import os

# Adafruit circutpython
import board
import busio

# Import sensor modules
import adafruit_mpl115a2
from adafruit_bme280 import basic as adafruit_bme280
import adafruit_vl53l1x
import adafruit_adxl34x

# Acquire the existing logger
try:
    logger = logging.getLogger(__name__)
except:
    logger = None
    print('Unable to acquire the global logger object, assuming that sensors.py is being run on its own')

# Main sensor program loop
def main():
    # Sensor information and init functions
    sensors = {
        'MPL115A2': {
            addr: 0x60
            type: 'temperature, pressure'
            init: adafruit_mpl115a2.MPL115A2
        }
        'BME280A': {
            addr: 0x77,
            type: 'outside temperature, pressure, humidity'
            init: adafruit_bme280.Adafruit_BME280_I2C
        }
        'BME280B': {
            addr: 0x76,
            type: 'inside temperature, pressure, humidity'
            init: adafruit_bme280.Adafruit_BME280_I2C
        }
        'VL53L1X': {
            addr: 0x29
            type: 'distance',
            init: adafruit_vl53l1x.VL53L1X
        }
        'ADXL34X': {
            addr: 0x53,
            type: 'acceleration',
            init: adafruit_adxl34x.ADXL345
        }
    }

    # Configure & initialize the sensors
    logging.info('Initializing sensors')

    # Begin i2c
    try:
        i2c = busio.I2C(board.SCL, board.SDA)
        logging.info('I2C interface ... OK')
    except: 
        logging.critical('Failed to enable i2c interface, the sensor thread will now crash')
        return

    # Query all the devices on the i2c bus
    i2cDevices = i2c.scan()

    # Sensors
    mpl115a2 = None
    bme280a = None
    bme280b = None
    vl53l1x = None
    adxl34x = None

    # For each sensor that we have defined
    for name, sensor in sensors:
        # If the address of the sensor is not in the i2c bus, we can skip it
        if sensor.addr not in i2cDevices:
            logging.info(f'{name} ({sensor.type}) was not detected on the i2c bus')
            continue
        # Attempt to initialize the sensor
        try:
            # Dynamic assignment to the sensor's variable using the init function defined in the sensors object
            globals()[name.lower()] = sensor.init(i2c, sensor.addr)
            logging.info(f'{name} ({sensor.type}) ... OK')
        except: 
            logging.error(f'Failed to enable {name} ({sensor.type}) sensor')

    logging.info('Sensor initialization complete')

    # Create the output directory if it does not exist yet
    os.system('mkdir -p ./data-sensors')
    # Start the sensor output file
    datafileName = './data-sensors/sensors-' + str(int(time.time() * 1000)) + '.csv'
    datafile = open(datafileName, 'w') 
    logging.info('Opened sensor data file for writing: ' + datafileName)

    # CSV header line
    csvheader = 'Time'
    if mpl115a2 != None: csvheader += ',MPL115A2 Temperature, MPL115A2 Pressure'
    if vl53l1x != None: csvheader += ',VL53L1X Distance'
    if bme280a != None: csvheader += ',Outside BME280 Temperature, Outside BME280 Pressure, Outside BME280 Humidity'
    if bme280b != None: csvheader += ',Inside BME280 Temperature, Inside BME280 Pressure, Inside BME280 Humidity'
    if adxl34x != None: csvheader += ',ADXL34X Accelerometer X-axis, ADXL34X Accelerometer Y-axis, ADXL34X Accelerometer Z-axis'
    datafile.write(csvheader + '\n')
    logging.info(f'Sensor file CSV columns are as follows: {csvheader}')

    # Sensor sample and data write loop
    logging.info('Beginning sensor polling and writing')
    while True:
        # Time axis
        csvline = str(int(time.time() * 1000))
        
        # Add entries to the CSV line based on the presence of those particular sensors
        if mpl115a2 != None: csvline += f',{mpl115a2.temperature},{mpl115a2.pressure}'
        if vl53l1x != None: csvline += f',{vl53l1x.distance}'
        if bme280a != None: csvline += f',{bme280a.temperature},{bme280a.pressure},{bme280a.relative_humidity}'
        if bme280b != None: csvline += f',{bme280b.temperature},{bme280b.pressure},{bme280b.relative_humidity}'
        if adxl34x != None: csvline += f',{adxl34x.acceleration[0]},{adxl34x.acceleration[1]},{adxl34x.acceleration[2]}'
        
        datafile.write(csvline + '\n')
        # Print the CSV line to the console if the file is running standalone
        if logger == None: print(csvline)

if __name__ == '__main__':
    main()
