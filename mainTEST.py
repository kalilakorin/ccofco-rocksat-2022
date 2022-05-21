#!/usr/bin/python
'''
    This is the main control script for the CC of CO RockSat 2021-2022 payload.
    Contributors:
        Jillian Frimml
        Skyler Puckett
        Konstantin Zaremski

    --- This product contains software from the previous payload written
        by Andrew Bruckbauer and Konstantin Zaremski for RockSat 2019 - 2021.

    Testing:
        The control program can be tested using the '--test' argument. Testing
        mode simulates a shutdown.

    Reset:
        The control program can be reset using the '--reset' argument.
        The reset argument clears any persisting save state so that operaiton
        can be tested as if running for the first time.
        $ python control.py --reset
        Flags can be supplied together (optional):
        $ python control.py --reset --test

    Functionality:
        This program controls all payload functionality. All individual software
        subsystems for other experiments are integrated as modules that run in
        their own sub processes/threads. Timer events should be listened to within
        this file and not any of the other sub modules in case changes need to be
        made to timing.
'''

# Import required modules
import time
import logging
from logging.handlers import RotatingFileHandler
import os
import multiprocessing as multiprocessing
import sys

# Import system modules
# import auxcam
# import sensors
# import fram

import RPi.GPIO as GPIO
from adafruit_motorkit import MotorKit
import armMotor
import subprocess
# import gopro2
# import goproTest

# import gopro

# Create a log folder if it does not exist yet
os.system('mkdir -p ./logs')
# Set up logging and log boot time
boottime = int(time.time())
rotatingFileHandler = RotatingFileHandler(
    filename=f'logs/rocksat_payload_{str(boottime)}.log',
    mode='a',
    maxBytes=20 * 1024 * 1024,
    backupCount=2,
    encoding='utf-8',
    delay=0
)
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s.%(msecs)03d][%(module)7s][%(levelname)8s]\t%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[rotatingFileHandler])

logger = logging.getLogger(__name__)

# Output all logs to console
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

logger.info(f'CC of CO payload finished booting at {boottime}\n')

def main():
    try:
        # Normal flight functionality
        te1 = 27  # TE-1
        lse = 22  # Limit Switch Extension
        te2 = 23  # TE-2
        lsr = 24  # Limit Switch Retraction
        ter = 17  # gopro activation
        am = 5  # arm motor inhibit GPIO pin (5)

        logger.info('Initializing GPIO pins...')
        try:
            motor = MotorKit()
            GPIO.setmode(GPIO.BCM)  # GPIO PIN NAMES
            GPIO.setup(ter, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # TE-R around 10 seconds
            GPIO.setup(te1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # TE-1 around +85 seconds
            GPIO.setup(lse, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Extension Limit Switch
            GPIO.setup(te2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # TE-2 around +220 seconds
            GPIO.setup(lsr, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Retraction Limit Switch
            # testing inhibits
            GPIO.setup(am, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   # motor inhibit
            logger.info('GPIO pins initialized... OK\n')
        except:
            logger.critical('Failed to initialize GPIO pins and motor hat.\n')
            return

        motor.motor1.throttle = 0

        # inhibit testing
        if GPIO.input(am):
            logger.info('Testing mode enabled: ' + str(int(time.time() * 1000)) + '\n')
            terDone = 1
            te1Done = 1
            lseDone = 1  # limit switch extension
            te2Done = 1
            lsrDone = 1  # limit switch retraction
        else:
            # normal flight functionality
            logger.info('Flight mode enabled: ' + str(int(time.time() * 1000)) + '\n')
            terDone = 0
            te1Done = 0
            lseDone = 0  # limit switch extension
            te2Done = 0
            lsrDone = 1  # limit switch retraction

        while True:
            if GPIO.input(te1):
                armMotor = multiprocessing.Process(target=armMotor.main)
                armMotor.start()
                break

        logger.info('All time events have been detected: ' + str(int(time.time() * 1000)) + '\n')
        GPIO.cleanup()
    except KeyboardInterrupt:
        print('Caught KeyboardInterrupt exiting')


#def initializeGPIO():

# def goproCall(motor):
#     # test address D1:70:A4:FC:21:4F
#     # flight address E3:BB:1E:0D:C8:52
#     logger.info('Calling GoPro thread...')
#     motor.motor4.throttle = 1.0
#     goproThread = multiprocessing.Process(target=gopro2.main)
#     goproThread.start()
#     time.sleep(15)
#     motor.motor4.throttle = 0
#     logger.info('GoPro motor off...\n')

def te1Call(motor):
    # set throttle (extension)
    motor.motor1.throttle = 1.0
    logger.info('Extension start: ' + str(int(time.time() * 1000)) + '\n')

def lseCall(motor):
    # set throttle (stop)
    motor.motor1.throttle = 0
    logger.info('Extension stop: ' + str(int(time.time() * 1000)) + '\n')

def te2Call(motor):
    # set throttle (retraction)
    motor.motor1.throttle = -1.0
    logger.info('Retraction start: ' + str(int(time.time() * 1000)) + '\n')

def lsrCall(motor):
    # set throttle (stop)
    motor.motor1.throttle = 0
    logger.info('Retraction stop detected: ' + str(int(time.time() * 1000)) + '\n')

# def rfCall(motor):
#     logger.info('Calling GoPro test thread...')
#     motor.motor4.throttle = 1.0
#     goprotestThread = multiprocessing.Process(target=goproTest.main)
#     goprotestThread.start()
#     time.sleep(15)
#     motor.motor4.throttle = 0
#     logger.info('GoPro motor test off...\n')

if __name__ == '__main__':
    # multiprocessing.set_start_method('fork')
    # processQueue = multiprocessing.Queue()
    main()
