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
import auxcam
import sensors
import fram

import RPi.GPIO as GPIO
from adafruit_motorkit import MotorKit
import subprocess
import gopro2

# import gopro
# import goprotest

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

# formatter = logging.Formatter('[%(asctime)s.%(msecs)03d][%(module)7s][%(levelname)8s]\t%(message)s')

logger = logging.getLogger(__name__)

# Output all logs to console
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

logger.info(f'CC of CO payload finished booting at {boottime}')


def main():
    try:
        multiprocessing.set_start_method('fork')
        processQueue = multiprocessing.Queue()
        # Accept command line arguments

        # If no command line arguments are passed the script will assume that it is running in
        arguments = sys.argv
        runAll = len(arguments) == 1

        if ('--auxcam' in arguments or runAll):
            auxcamThread = multiprocessing.Process(target=auxcam.main)
            auxcamThread.start()

        # Secondary experiment (radiation RAM)
        if ('--fram' in arguments or runAll):
            framExperimentThread = multiprocessing.Process(target=fram.main)
            framExperimentThread.start()

        # Tertiary experiment (sensors)
        if ('--sensors' in arguments or runAll):
            sensorThread = multiprocessing.Process(target=sensors.main)
            sensorThread.start()

        # Normal flight functionality
        te1 = 27  # TE-1
        lse = 22  # Limit Switch Extension
        te2 = 23  # TE-2
        lsr = 24  # Limit Switch Retraction
        ter = 17  # gopro activation

        # inhibits for testing
        #rf = 6  # RF inhibit GPIO pin  (6)
        #am = 5  # arm motor inhibit GPIO pin (5)

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
            #GPIO.setup(rf, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   # RF inhibit
            #GPIO.setup(am, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   # motor inhibit
            logger.info('GPIO pins initialized... OK')
        except:
            logger.critical('Failed to initialize GPIO pins and motor hat.')
            return

        # normal flight functionality
        terDone = 0
        te1Done = 0
        lseDone = 0 #limit switch extension
        te2Done = 0
        lsrDone = 0 #limit switch retraction

        # inhibit testing
        #if GPIO.input(am):
        #    logger.info('Testing mode enabled: ' + str(int(time.time() * 1000)))
            # attempt test 1
        #    while True:
        #        try:
        #            logger.info('Testing RF in first test: ' + str(int(time.time() * 1000)))
        #            rfCall()
        #            break
        #        except:
        #            logger.info('Waiting for power to test RF')
        #            sleep(15)

        while True:
            # attempt test 2 - may need to be used in conjunction with the above as well
            # if GPIO.input(am): # and GPIO.input(rf): # i don't think this second half is correct
            #    logger.info('Testing RF: ' + str(int(time.time() * 1000)))
            #    rfCall()
            #    break
            if GPIO.input(ter) and terDone == 0:
                logger.info('TE-R detected')
                goproCall()
                terDone = 1
            if GPIO.input(te1) and te1Done == 0:
                logger.info('TE-1 detected')
                te1Call()
                te1Done = 1
            if GPIO.input(lse) and lseDone == 0:
                logger.info('Limit switch detected')
                lseCall()
                lseDone = 1
            if GPIO.input(te2) and te2Done == 0:
                logger.info('TE-2 detected')
                te2Call()
                te2Done = 1
            if GPIO.input(lsr) and lsrDone == 0:
                logger.info('Limit switch detected')
                lsrCall()
                lsrDone = 1
                break

        GPIO.cleanup()
    except KeyboardInterrupt:
        print('Caught KeyboardInterrupt exiting')


#def initializeGPIO():

def goproCall():
    # test address D1:70:A4:FC:21:4F
    # flight address E3:BB:1E:0D:C8:52
    logger.info('Calling GoPro thread...')
    goproThread = multiprocessing.Process(target=gopro2.main)
    goproThread.start()

def te1Call():
    # set throttle (extension)
    motor.motor1.throttle = 1.0
    logger.info('Extension start: ' + str(int(time.time() * 1000)))

def lseCall():
    # set throttle (stop)
    motor.motor1.throttle = 0
    logger.info('Extension stop: ' + str(int(time.time() * 1000)))

def te2Call():
    # set throttle (retraction)
    motor.motor1.throttle = -1.0
    logger.info('Retraction start: ' + str(int(time.time() * 1000)))

def lsrCall():
    # set throttle (stop)
    motor.motor1.throttle = 0
    logger.info('Retraction stop detected: ' + str(int(time.time() * 1000)))

def rfCall():
    logger.info('Calling GoPro test thread...')
    goprotestThread = multiprocessing.Process(target=goprotest.main)
    goprotestThread.start()

if __name__ == '__main__':
    main()
