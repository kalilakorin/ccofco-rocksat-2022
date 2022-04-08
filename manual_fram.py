'''
    CC of CO RockSat 2022
'''

SOURCE_FILE_PATH = 'monalisa.jpg'

# Import dependencies
from ast import arguments
from adafruit_extended_bus import ExtendedI2C as I2C
import adafruit_fram
import os
import sys

# Init i2c
def init():
    # Configure the I2C busses
    i2c = {}
    # I2C interface A
    try:
        i2c['bus0'] = I2C(1)
        print('I2C interface A ... OK')
    except Exception as error:
        print('Failed to enable i2c interface A')
        print('  ' + str(error))
        # Set the interface as None to indicate that it is not working
        i2c['bus0'] = None
    # I2C interface B
    try:
        i2c['bus1'] = I2C(4)
        print('I2C interface B ... OK')
    except Exception as error:
        print('Failed to enable i2c interface B')
        print('  ' + str(error))
        # Set the interface as None to indicate that it is not working
        i2c['bus1'] = None
    # I2C interface C
    try:
        i2c['bus2'] = I2C(5)
        print('I2C interface C ... OK')
    except Exception as error:
        print('Failed to enable i2c interface C')
        print('  ' + str(error))
        # Set the interface as None to indicate that it is not working
        i2c['bus2'] = None

    # Build an array of board classes dynamically
    fram = [None] * 24
    # For each i2c bus
    for busNo in range(0, 3):
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
                print(f'FRAM{str(globalBoardNo)} size: {str(len(fram[globalBoardNo]))} bytes')
            except Exception as error:
                fram[globalBoardNo] = None
                print(f'FRAM{str(globalBoardNo)} not detected. {error}')
    
    return fram

# Byte array from file
def fileByteArray(path):
    # Creating an array of the bytes that make up monalisa.jpg
    sourceByteArray = bytearray()
    try:
        with open(path, 'rb') as sourceFile:
            sourceByteArray = sourceFile.read()
            print('Finished reading ' + path)
    except IOError:
        print('Failed to read ' + path)
    return sourceByteArray

def writeByteArray(outputByteArray, path):
    outputFile = open(path, 'wb')
    outputFile.write(outputByteArray)
    outputFile.close()

# Write to FRAM
def write():
    fram = init()
    sourceByteArray = fileByteArray(SOURCE_FILE_PATH)

    print('** Beginning write')
    for framBoardIndex in range(0, len(fram)):
        framBoard = fram[framBoardIndex]
        if framBoard != None:
            try:
                framBoard[0:len(sourceByteArray)] = sourceByteArray[0:len(sourceByteArray)]
                print(f'Wrote to board {str(framBoardIndex)}')
            except Exception as err:
                print(f'Failed write to FRAM board {str(framBoardIndex)}. Error: "{str(err)}"')
    print('** Finished writing to all boards')

# Read from FRAM
def read():
    fram = init()

    sourceByteArray = fileByteArray(SOURCE_FILE_PATH)

    os.system('mkdir -p ./manual-fram-data')
    
    print('** Beginning read from all boards')
    for framBoardIndex in range(0, len(fram)):
        framBoard = fram[framBoardIndex]
        if framBoard != None:
            cooked = bytearray()
            for byteIndex in range(0, len(sourceByteArray)):
                cooked += framBoard[byteIndex]
            print('Read from board ' + str(framBoardIndex))
            filePath = f'./manual-fram-data/fram_{str(framBoardIndex)}.jpg'
            writeByteArray(cooked, filePath)
            print('Wrote to ' + filePath) 
    print('** Finished read from all boards')

# Entry point
if __name__ == '__main__':
    arguments = sys.argv
    if ('--write' in arguments):
        write()
    elif ('--read' in arguments):
        read()
    else:
        print('Nothing done, no valid command line options supplied.')
        print('Please use --write or --read')
