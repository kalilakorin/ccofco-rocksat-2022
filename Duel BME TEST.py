

import board
import busio
from adafruit_bme280 import basic as adafruit_bme280

i2c = busio.I2C(board.SCL, board.SDA)

bme280a = adafruit_bme280.Adafruit_BME280_I2C(i2c) #adress 0x77
bme280a.sea_level_pressure = 1013.25

bme280b = adafruit_bme280.Adafruit_BME280_I2C(i2c) #adress 0x77
bme280b.sea_level_pressure = 1013.25


for i in range(50):
    print(str(bme280a.temperature) + ' a')
    print(str(bme280b.temperature) + ' b')
