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
import logging
import RPi.GPIO as GPIO
from adafruit_motorkit import MotorKit

print("Start...\n\n")
# try:
#     logger = logging.getLogger(__name__)
# except:
#     logger = None
#     print('Unable to acquire the global logger object, assuming that armMotor.py is being run on its own')


''' might need to enable i2c as well?  I am not sure.  I know the motor hat is
 addressed in I2C but the git I was using did not have I2C enabled'''


# Main motor hat program loop
def main():
    # Configure & initialize the motor hat and GPIO pins
    logging.info('Initializing motor hat')

    te1 = 27 # TE-1
    lse = 22 # Limit Switch Extension
    te2 = 23 # TE-2
    lsr = 24 # Limit Switch Retraction

    # GPIO pin assignment
    #try:
    motor = MotorKit()
    GPIO.setmode(GPIO.BCM)  #GPIO PIN NAMES
    GPIO.setup (te1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # TE-1 around +85 seconds
    GPIO.setup (lse, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Extension Limit Switch
    GPIO.setup (te2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # TE-2 around +220 seconds
    GPIO.setup (lsr, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Retraction Limit Switch

    #except:
        #logger.critical('Failed to initialize GPIO pins and motor hat ')
       # return



    # wait for TE-1 signal
    while True:
        if GPIO.input(te1):
            break

    #logger.info ('TE-1 detected: ' + str (int (time.time () * 1000)))
    # set throttle (extension)
    motor.motor1.throttle = 1.0
    print ("TE-1 Detected...\n\n")
    # wait for extension limit switch activation
    while True:
        if GPIO.input(lse):
            break
    #logger.info ('Extension stop detected: ' + str (int (time.time () * 1000)))
    # set throttle (stop)
    motor.motor1.throttle = 0
    print ("Extension Stop Detected...\n\n")
    # wait for TE-2 signal
    while True:
        if GPIO.input(te2):
            break
    #logger.info ('TE-2 detected: ' + str (int (time.time () * 1000)))
    # set throttle (retraction)
    motor.motor1.throttle = -1.0
    print ("TE-2 Detected...\n\n")
    # wait for retraction limit switch activation
    while True:
        if GPIO.input(lsr):
            break
    #logger.info ('Retraction stop detected: ' + str (int (time.time () * 1000)))
    # set throttle (stop)
    motor.motor1.throttle = 0
    print ("Retraction Stop Detected...\n\n")
    GPIO.cleanup()



if __name__ == '__main__':
    main()
