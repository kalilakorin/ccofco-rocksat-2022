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
import multiprocessing as multiprocessing

import board
import busio

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

    # Begin i2c
    try:
        i2c = busio.I2C(board.SCL, board.SDA)
        logging.info('I2C interface ... OK')
    except: 
        logging.critical('Failed to enable i2c interface, the sensor thread will now crash')
        return

    # Build an array of board classes dynamically
    fram = [None] * 8
    for boardNo in range(0, 8):
        try:
            fram[boardNo] = adafruit_fram.FRAM_I2C(i2c, 80 + boardNo) # 0x50 is 80 as int
            logging.info(f'FRAM{str(boardNo)} size: {str(len(fram[boardNo]))} bytes')
        except Exception as error:
            fram[boardNo] = None
            logging.error(f'FRAM{str(boardNo)} not detected')

    # ** Define all sub methods used throughout experiment tirals
    # Write the source image to the provided FRAM board object
    def writeBoard(framBoard):
        i = 0
        for byte in sourceByteArray:
            framBoard[i] = byte
            i += 1

    # Read back the contents of all FRAM boards and write to file
    def readBoard(framBoard, boardNo, trialNo):
        cooked = framBoard[0:len(sourceByteArray)]
        resultFile = open(f'data-fram__trial{str(trialNo)}__board{str(boardNo)}.jpg', 'wb')
        resultFile.write(bytes(cooked))
        resultFile.close()

    # Write all zeros to the FRAM boards present
    def eraseBoard(framBoard):
        framBoard[0:len(fram)] = [0] * len(fram)

    experimentMultiThreadingQueue = multiprocessing.Queue()
    experimentTrial = 1
    while True:
        logging.info(f'Beginning FRAM experiment trial no. {str(experimentTrial)}')
            
        # Create threads for writing source image
        threads = []
        for framBoard in fram:
            if framBoard != None: threads.append(multiprocessing.Process(target=writeBoard, args=(framBoard)))
        # Wait for all threads to close
        for thread in threads:
            thread.join()
        
        # Create threads for reading data
        threads = []
        i = 0
        for framBoard in fram:
            if framBoard != None: threads.append(multiprocessing.Process(target=readBoard, args=(framBoard, i, experimentTrial)))
            i += 1
        # Wait for all threads to close
        for thread in threads:
            thread.join()

        # Create threads for erasing all boards
        threads = []
        for framBoard in fram:
            if framBoard != None: threads.append(multiprocessing.Process(target=eraseBoard, args=(framBoard)))
        # Wait for all threads to close
        for thread in threads:
            thread.join()

        experimentTrial += 1

if __name__ == '__main__':
    main()