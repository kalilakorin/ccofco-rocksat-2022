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
import sys
import multiprocessing as multiprocessing

from adafruit_extended_bus import ExtendedI2C as I2C
import adafruit_fram

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

    # Configure the I2C busses
    i2c = {}
    # I2C interface A
    try:
        i2c['bus0'] = I2C(1)
        logging.info('I2C interface A ... OK')
    except Exception as error:
        logging.critical('Failed to enable i2c interface A')
        logging.critical('Error: ' + str(error))
        # Set the interface as None to indicate that it is not working
        i2c['bus0'] = None
    # I2C interface B
    try:
        i2c['bus1'] = I2C(4)
        logging.info('I2C interface B ... OK')
    except Exception as error:
        logging.critical('Failed to enable i2c interface B')
        logging.critical('Error: ' + str(error))
        # Set the interface as None to indicate that it is not working
        i2c['bus1'] = None
    # I2C interface C
    try:
        i2c['bus2'] = I2C(5)
        logging.info('I2C interface C ... OK')
    except Exception as error:
        logging.critical('Failed to enable i2c interface C')
        logging.critical('Error: ' + str(error))
        # Set the interface as None to indicate that it is not working
        i2c['bus2'] = None

    # Find all i2c devices on the busses that are connected
    if i2c['bus0'] != None: i2c['devices0'] = i2c['bus0'].scan()
    if i2c['bus1'] != None: i2c['devices1'] = i2c['bus1'].scan()
    if i2c['bus2'] != None: i2c['devices2'] = i2c['bus2'].scan()

    # Build an array of board classes dynamically
    # Only configure bus0 if --single-fram-bus argument is supplied
    busCount = 1 if '--single-fram-bus' in sys.argv else 3
    fram = [None] * 24
    # For each i2c bus
    for busNo in range(0, busCount):
        # If the i2c bus was not configured, do nothing and move on to the next bus
        if i2c['bus' + str(busNo)] == None: continue
        # For each board that should be connected to the i2c bus
        for boardNo in range(0, 8):
            # Global board no based on the position in the loops eg.
            # bus0 contains fram0   thru  fram7
            # bus1 contains fram8   thru  fram16
            # bus2 contains fram16  thru  fram21
            globalBoardNo = boardNo + (8 * busNo)
            try:
                fram[globalBoardNo] = adafruit_fram.FRAM_I2C(i2c['bus' + str(busNo)], 0x50 + boardNo)
                logging.info(f'FRAM{str(globalBoardNo)} size: {str(len(fram[globalBoardNo]))} bytes')
            except Exception as error:
                fram[globalBoardNo] = None
                logging.error(f'FRAM{str(globalBoardNo)} not detected. {error}')

    # Debug exit
    logging.info('DEBUG CODE MODIFICATIONS, exiting... ~KZ')
    return

    # ** Define all sub methods used throughout experiment tirals
    # Write the source image to the provided FRAM board object
    def writeBoard(framBoard):
        try:
            framBoard[0:len(sourceByteArray)] = sourceByteArray[:]
        except Exception as err:
            logging.error(f'Failed write to {str(framBoard)}: "{str(err)}"')

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