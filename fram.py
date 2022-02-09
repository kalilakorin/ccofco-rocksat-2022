'''
    This file controls the secondary (radiation) experiment
    Contributors:
        Jillian Frimml
        Skyler Puckett
        Konstantin Zaremski
'''

# Import modules
from time import sleep
import time
import logging
import os
import multiprocessing as multiprocessing

import board
import busio

import adafruit_fram
import adafruit_tca9548a

# Configuration
FRAM_COOK_DURATION = 0

# Acquire the existing logger
try:
    logger = logging.getLogger(__name__)
except:
    logger = None
    print('Unable to acquire the global logger object, assuming that sensors.py is being run on its own')

# Main FRAM experiment program loop
def main():
    # Configure & initialize the FRAM boards
    logging.info(f'Initializing FRAM experiment')

    # Creating an array of the bytes that make up monalisa.jpg
    sourceByteArray = []
    try:
        with open('monalisa.jpg', 'rb') as sourceFile:
            byte = sourceFile.read(1)
            while byte:
                byte = sourceFile.read(1)
                sourceByteArray.append(int.from_bytes(byte, 'big'))
        logging.info(f'Finished building array from input file, {str(len(sourceByteArray))} bytes')
    except IOError:
        logging.critical('Unable to read in source image (monalisa.jpg)')

    # Create the output directory if it does not exist yet
    os.system('mkdir -p ./data-fram')

    # Begin i2c
    try:
        i2c = busio.I2C(board.SCL, board.SDA)
        logging.info('I2C interface ... OK')
    except: 
        logging.critical('Failed to enable i2c interface, the sensor thread will now crash')
        return

    # Find all i2c devices
    i2cDevices = i2c.scan()

    # Build an array of board classes dynamically
    fram = [None] * 24
    for channelNo in range(0, 3):
        address = 112 + channelNo
        # If there is no i2c device at the intended address, we can assume that there is not a multiplexer there
        if (address not in i2cDevices):
            logging.error(f'Multiplexer {str(channelNo)} was not detected, skipping')
            continue
        # Initialize the multiplexer
        try:
            tca = adafruit_tca9548a.TCA9548A(i2c, address)
            logging.info(f'Initialized multiplexer {str(channelNo)}')
        except:
            # If we can not get the multiplexer to work move on because we will not be able to get any boards off of it
            logging.error(f'Failed to initialize multiplexer {str(channelNo)}')
            continue
        # For each board that should be connected to the
        for boardNo in range(0, 8):
            globalBoardNo = boardNo + (8 * channelNo)
            try:
                fram[globalBoardNo] = adafruit_fram.FRAM_I2C(tca[boardNo], 80)
                logging.info(f'FRAM{str(globalBoardNo)} size: {str(len(fram[globalBoardNo]))} bytes')
            except Exception as error:
                fram[globalBoardNo] = None
                logging.error(f'FRAM{str(globalBoardNo)} not detected. {error}')

    # ** Define all sub methods used throughout experiment tirals
    # Write the source image to the provided FRAM board object
    def writeBoard(framBoard):
        try:
            framBoard[0:len(sourceByteArray)] = sourceByteArray[:]
        except:
            logging.error(f'Failed write to {str(framBoard)}')

    # Read back the contents of all FRAM boards and write to file
    def readBoard(framBoard, boardNo, trialNo):
        cooked = framBoard[0:len(sourceByteArray)]
        resultFile = open(f'data-fram__trial{str(trialNo)}__board{str(boardNo)}__{str(int(time.time()))}.jpg', 'wb')
        resultFile.write(bytes(cooked))
        resultFile.close()

    # Write all zeros to the FRAM boards present
    # -- this function is no longer used
    def eraseBoard(framBoard):
        framBoard[0:len(fram)] = [0] * len(fram)

    # Create threads for writing source image
    # The source image is written to each FRAM board at the power-on of the payload
    # Then it is read back throughout the experiment
    startWriteTime = time.time()
    logger.info(f'Beginning write of source image to FRAM boards at {str(int(startWriteTime))}')
    threads = []
    for framBoard in fram:
        if framBoard != None:
            framWriteThread = multiprocessing.Process(target=writeBoard, args=(framBoard,))
            framWriteThread.start()
            threads.append(framWriteThread)
    # Wait for all threads to close
    for thread in threads:
        thread.join()
    endWriteTime = time.time()
    logger.info(f'Finished writing source image to all FRAM boards at {str(int(endWriteTime))} ({str(int(endWriteTime - startWriteTime))}ms. elapsed)')

    # Main experiment loop
    experimentTrial = 1
    return
    while True:
        logging.info(f'Beginning FRAM experiment trial no. {str(experimentTrial)}')
            
        # Create threads for reading data
        threads = []
        i = 0
        for framBoard in fram:
            if framBoard != None:
                thread = multiprocessing.Process(target=readBoard, args=(framBoard, i, experimentTrial))
                thread.start()
                threads.append(thread)
            i += 1
        # Wait for all threads to close
        for thread in threads:
            thread.join()

        experimentTrial += 1

if __name__ == '__main__':
    main()