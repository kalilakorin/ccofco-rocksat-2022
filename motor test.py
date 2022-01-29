# test the motor hat functionality

import time
from adafruit_motorkit import MotorKit

motor = MotorKit()

motor.motor1.throttle = 0.5
time.sleep(5)
motor.motor1.throttle = 0
time.sleep(2)
motor.motor1.throttle = -0.5
time.sleep(5)
motor.motor1.throttle = 0



