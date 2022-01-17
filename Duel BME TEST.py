

import board
import busio
from adafruit_bme280 import basic as adafruit_bme280

i2c = busio.I2C(board.SCL, board.SDA)

bme280a = adafruit_bme280.Adafruit_BME280_I2C(i2c, 0x77) #adress 0x77

#bme280b = adafruit_bme280.Adafruit_BME280_I2C(i2c, 0x76) #adress 0x76

for i in range(50):
    print(str(bme280a.temperature) + ' a')
    #print(str(bme280b.temperature) + ' b')
