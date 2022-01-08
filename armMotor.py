"""
    This file handles all motor functions with timer events
    Contributors:
        Jillian Frimml
        Skyler Puckett
        Konstantin Zaremski
        https://www.ics.com/blog/control-raspberry-pi-gpio-pins-python
        https://github.com/adafruit/Adafruit_CircuitPython_MotorKit
"""

# Import modules
import time
import RPi.GPIO as GPIO
from adafruit_motorkit import MotorKit

try:
    logger = logging.getLogger(__name__)
except:
    logger = None
    print('Unable to acquire the global logger object, assuming that armMotor.py is being run on its own')


# Main motor hat program loop
def main():
    # Configure & initialize the motor hat and GPIO pins
    logging.info('Initializing motor hat')
    # GPIO pin assignment
    try:
        GPIO.setmode(GPIO.BOARD)  # Pin# not GPIO#
        GPIO.setup(13, GPIO.IN)  # TE-1 around +85 seconds
        GPIO.setup(15, GPIO.IN)  # Extension Limit Switch
        GPIO.setup(16, GPIO.IN)  # TE-2 around +220 seconds
        GPIO.setup(18, GPIO.IN)  # Retraction Limit Switch
        motor = MotorKit()
    except:
        logger.critical('Failed to initialize GPIO pins and motor hat ')



    # wait for TE-1 signal
    while True:
        if GPIO.input(13):
            break
    # set throttle (extension)
    motor.motor1.throttle = 1.0
    # wait for extension limit switch activation
    while True:
        if GPIO.input(15):
            break
    # set throttle (stop)
    motor.motor1.throttle = 0
    # wait for TE-2 signal
    while True:
        if GPIO.input(16):
            break
    # set throttle (retraction)
    motor.motor1.throttle = -1.0
    # wait for retraction limit switch activation
    while True:
        if GPIO.input(18):
            break
    # set throttle (stop)
    motor.motor1.throttle = 0

    GPIO.cleanup()


if __name__ == '__main__':
    main()
