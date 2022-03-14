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
import serial  # might be needed for telemetry

# Adafruit circutpython
import board
import busio

# Import sensor modules
import adafruit_mpl115a2
from adafruit_bme280 import basic as adafruit_bme280
import adafruit_vl53l1x
import adafruit_adxl34x

ser = serial.Serial(
        port='/dev/ttyS0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate = 19200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)

# Acquire the existing logger
try :
    logger = logging.getLogger (__name__)
except :
    logger = None
    print ('Unable to acquire the global logger object, assuming that sensors.py is being run on its own')

string = "Sensor PAGE TEST"
ser.write(string.encode('utf-8'))
print("STRING WRITTEN to SERIAL PORT")

# Main sensor program loop
def main () :
    # Configure & initialize the sensors
    logging.info ('Initializing sensors')

    # Begin i2c
    try :
        i2c = busio.I2C (board.SCL, board.SDA)
        logging.info ('I2C interface ... OK')
    except :
        logging.critical ('Failed to enable i2c interface, the sensor thread will now crash')
        return
    # Init mpl sensor
    try :
        mpl115a2 = adafruit_mpl115a2.MPL115A2 (i2c)
        logging.info ('MPL115A2 (temperature, pressure) ... OK')
    except :
        mpl115a2 = None
        logging.error ('Failed to enable MPL115A2 sensor')
    # Init bme280 Outside
    try :
        bme280a = adafruit_bme280.Adafruit_BME280_I2C (i2c)  # address 0x77 DEFAULT (outside)
    except :
        bme280a = None
        logging.error ('Failed to enable "outside" BME280 (temperature, pressure, humidity) sensor')
    # Init bme280 Inside
    try :
        bme280b = adafruit_bme280.Adafruit_BME280_I2C (i2c, 0x76)  # address 0x76 ALTERNATIVE (inside EBox)
    except :
        bme280b = None
        logging.error ('Failed to enable BME280 (temperature, pressure, humidity) sensor')
    # Init vl53l1x distance sensor
    try :
        vl53l1x = adafruit_vl53l1x.VL53L1X (i2c)
        vl53l1x.start_ranging ()
    except :
        vl53l1x = None
        logging.error ('Failed to enable VL53L1X (distance) sensor')
    # ADXL34x accelerometer
    try :
        adxl34x = adafruit_adxl34x.ADXL345 (i2c)
    except :
        adxl34x = None
        logging.error ('Failed to enable ADXL34X (accelerometer) sensor')

    logging.info ('Sensors initialized')

    # Create the output directory if it does not exist yet
    os.system ('mkdir -p ./data-sensors')
    # Start the sensor output file
    datafileName = './data-sensors/sensors-' + str (int (time.time () * 1000)) + '.csv'
    datafile = open (datafileName, 'w')
    logging.info ('Opened sensor data file for writing: ' + datafileName)

    # CSV header line
    csvheader = 'Time'
    if mpl115a2 != None : csvheader += ',MPL115A2 Temperature, MPL115A2 Pressure'
    if vl53l1x != None : csvheader += ',vl53l1x Distance'
    if bme280a != None : csvheader += ',Outside BME280 Temperature, Outside BME280 Pressure, Outside BME280 Humidity'
    if bme280b != None : csvheader += ',Inside BME280 Temperature, Inside BME280 Pressure, Inside BME280 Humidity'
    if adxl34x != None : csvheader += ',adxl34x Accelerometer X-axis, adxl34x Accelerometer Y-axis, adxl34x Accelerometer Z-axis'

    datafile.write (csvheader + '\n')
    logging.info (f'Sensor file CSV columns are as follows: {csvheader}')

    # Sensor sample and data write loop
    logging.info ('Beginning sensor polling and writing (1000 samples/second)')

    count = 0
    while True :
        # Time axis
        csvline = str (int (time.time () * 1000))

        # Add entries to the CSV line based on the presence of those particular sensors
        if mpl115a2 != None : csvline += f',{mpl115a2.temperature},{mpl115a2.pressure}'
        if vl53l1x != None : csvline += f',{vl53l1x.distance}'
        if bme280a != None : csvline += f',{bme280a.temperature},{bme280a.pressure},{bme280a.relative_humidity}'
        if bme280b != None : csvline += f',{bme280b.temperature},{bme280b.pressure},{bme280b.relative_humidity}'
        if adxl34x != None : csvline += f',{adxl34x.acceleration[0]},{adxl34x.acceleration[1]},{adxl34x.acceleration[2]}'

        datafile.write (csvline + '\n')
        # Print the CSV line to the console if the file is running standalone
        if logger == None : print (csvline)
        sleep (0.001)

        if count % 1000 == 0:
            serial_string = ""
            if mpl115a2 != None :  serial_string += f',{mpl115a2.temperature},{mpl115a2.pressure}'
            if vl53l1x != None : serial_string += f',{vl53l1x.distance}'
            if bme280a != None : serial_string += f',{bme280a.temperature},{bme280a.pressure},{bme280a.relative_humidity}'
            if bme280b != None : serial_string += f',{bme280b.temperature},{bme280b.pressure},{bme280b.relative_humidity}'
            if adxl34x != None : serial_string += f',{adxl34x.acceleration[0]},{adxl34x.acceleration[1]},{adxl34x.acceleration[2]}'
            if True : serial_string += "TEST" + str(count)
            ser.write(serial_string.encode('utf-8'))
            print (serial_string)
        count += 1


if __name__ == '__main__' :
    main ()
