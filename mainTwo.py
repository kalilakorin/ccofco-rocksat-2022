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
import gopromain as gopro

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

        # Arm Motor functions
        te1 = 27  # TE-1
        gppower = 16 # is the original power
        lse = 22  # Limit Switch Extension
        te2 = 23  # TE-2
        lsr = 24  # Limit Switch Retraction
        ter = 17  # gopro activation

        logger.info('Initializing GPIO pins...')
        try:
            motor = MotorKit()
            GPIO.setmode(GPIO.BCM)  # GPIO PIN NAMES
            GPIO.setup(ter, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # TE-R around 10 seconds
            GPIO.setup(gppower, GPIO.OUT)                         # power to the gopro camera
            GPIO.setup(te1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # TE-1 around +85 seconds
            GPIO.setup(lse, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Extension Limit Switch
            GPIO.setup(te2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # TE-2 around +220 seconds
            GPIO.setup(lsr, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Retraction Limit Switch
            logger.info('GPIO pins initialized... OK')
        except:
            logger.critical('Failed to initialize GPIO pins and motor hat.')
            return

        GPIO.output(gppower, GPIO.LOW)
        terDone = 0
        te1Done = 0
        lseDone = 0 #limit switch extension
        te2Done = 0
        lsrDone = 0 #limit switch retraction

        while True:
            if GPIO.input(ter) and terDone == 0:
                logger.info('TER detected')
                GPIO.output(gppower, GPIO.HIGH)
                time.sleep(5)
                print('Slept 5 sec')
                time.sleep(5)
                print('Slept 10 sec')
                time.sleep(5)
                print('Slept 15 sec')
                goproCall()
                GPIO.output(gppower, GPIO.LOW)
                terDone = 1
            if GPIO.input(te1) and te1Done == 0:
                logger.info('TE1 detected, extension start')
                te1Done = 1
            if GPIO.input(lse) and lseDone == 0:
                logger.info('Limit switch detected, extension stop')
                lseDone = 1
            if GPIO.input(te2) and te2Done == 0:
                logger.info('TE2 detected, retraction start')
                te2Done = 1
            if GPIO.input(lsr) and lsrDone == 0:
                logger.info('Limit switch detected, retraction stop')
                lsrDone = 1

        # gopro recording start
        # if ('--gopro' in arguments or runAll):
        #     goproThread = multiprocessing.Process(target=gopro.main)
        #     goproThread.start()

        # gopro wallops RF testing start
        # if ('--goprotest' in arguments or runAll):
        #     goprotestThread = multiprocessing.Process(target=goprotest.main)
        #     goprotestThread.start()

        # Prim
        # if framExperimentThread: framExperimentThread.join()
        # p1.terminate()
    except KeyboardInterrupt:
        print('Caught KeyboardInterrupt exiting')


#def initializeGPIO():

def goproCall():
    # test address D1:70:A4:FC:21:4F
    # flight address E3:BB:1E:0D:C8:52
    logger.info('Record starting...')
    while True:
        subprocess.call(f'python3 gopromain.py --verbose -a "D1:70:A4:FC:21:4F" -c "preset maxvideo" -c "record start"', shell=True)
        time.sleep(5)

def motor():
    # wait for ter signile
    while True:
        if GPIO.input(ter):
            break
    # call
    subprocess.call(f'python3 gopromain.py --verbose -a "D1:70:A4:FC:21:4F" -c "preset maxvideo" -c "record start"',
                    shell=True)

    time.sleep(5)
    subprocess.call(f'python3 gopromain.py --verbose -a "D1:70:A4:FC:21:4F" -c "preset maxvideo" -c "record start"',
                    shell=True)

    # wait for TE-1 signal
    while True:
        if GPIO.input(te1):
            break

    logger.info('TE-1 detected: ' + str(int(time.time() * 1000)))
    # set throttle (extension)
    motor.motor1.throttle = 1.0
    print("TE-1 Detected...\n\n")
    # wait for extension limit switch activation
    while True:
        if GPIO.input(lse):
            break
    logger.info('Extension stop detected: ' + str(int(time.time() * 1000)))
    # set throttle (stop)
    motor.motor1.throttle = 0
    print("Extension Stop Detected...\n\n")
    # wait for TE-2 signal
    while True:
        if GPIO.input(te2):
            break
    logger.info('TE-2 detected: ' + str(int(time.time() * 1000)))
    # set throttle (retraction)
    motor.motor1.throttle = -1.0
    print("TE-2 Detected...\n\n")
    # wait for retraction limit switch activation
    while True:
        if GPIO.input(lsr):
            break
    logger.info('Retraction stop detected: ' + str(int(time.time() * 1000)))
    # set throttle (stop)
    motor.motor1.throttle = 0
    print("Retraction Stop Detected...\n\n")
    GPIO.cleanup()


if __name__ == '__main__':
    main()
