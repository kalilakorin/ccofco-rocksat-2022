

import board
import busio
from adafruit_bme280 import basic as adafruit_bme280

i2c = busio.I2C(board.SCL, board.SDA)

bme280 = adafruit_bme280.Adafruit_BME280_I2C(0x76) #adress 0x77
bme280.sea_level_pressure = 1013.25

bme280 = adafruit_bme280.Adafruit_BME280_I2C(0x77) #adress 0x77
bme280.sea_level_pressure = 1013.25
        