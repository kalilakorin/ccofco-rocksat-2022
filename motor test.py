# test the motor hat functionality

import time
from adafruit_motorkit import MotorKit

motor = MotorKit()

motor.motor1.throttle = 0.5
sleep(5)
motor.motor1.throttle = 0
sleep(2)
motor.motor1.throttle = -0.5
sleep(5)

