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

    experimentTrial = 1
    while True:
        logging.info(f'Beginning FRAM experiment trial no. {str(experimentTrial)}')
        # Write the source image each FRAM board present in the array
        for framBoard in fram:
            if framBoard != None: framBoard[0:len(sourceByteArray)] = sourceByteArray
        
        sleep(FRAM_COOK_DURATION)

        # Read back the contents of all FRAM boards
        returned = [None] * 8
        boardNo = 0
        for framBoard in fram:
            if framBoard != None:
                cooked = framBoard[0:len(sourceByteArray)]
                returned[boardNo] = cooked
            boardNo += 1

        print(returned)

        # Write all zeros to the FRAM boards present
        for framBoard in fram:
            if framBoard != None: framBoard[0:len(fram)] = [0] * len(fram)

        experimentTrial += 1

if __name__ == '__main__':
    main()