'''
    Post flight analysis of FRAM experiment data.
'''

# Import dependencies
from audioop import add
import os

def main():
    # Creating an array of the bytes that make up monalisa.jpg
    sourceByteArray = bytearray()
    try:
        with open('monalisa.jpg', 'rb') as sourceFile:
            sourceByteArray = sourceFile.read()
        print(f'Finished building array from input file, {str(len(sourceByteArray))} bytes')
        print('This will be used as the control.')
    except IOError:
        print('Unable to read in source image (monalisa.jpg)')
    
    # Get a list of all the files in the output directory
    outputFiles = os.listdir('./data-fram')
    
    # For each item in the output directory
    for file in outputFiles:
        # If the file ends in JPG
        if file[-4:] == '.jpg':
            try:
                filePath = './data-fram/' + file 
                
                # Build the byte array of the image currently being analyzed
                currentByteArray = bytearray()
                with open(filePath, 'rb') as outputFile:
                    currentByteArray = outputFile.read()
                print(f'Finished reading output image: {filePath}')
                
                # Loop through the length of the source image
                passing = False
                for addr in range(0, len(sourceByteArray)):
                    if sourceByteArray[addr] != currentByteArray[addr]:
                        # If there is a bit flip, is not pass
                        passing = False
                        print(f'-- Anomaly at {hex(addr)}:')
                        print(f'---- CONTROL:  {str(sourceByteArray[addr])}')
                        print(f'---- ACTUAL:   {str(currentByteArray[addr])}')
                # Notify
                resultText = 'PASS' if passing else 'FAIL'
                print(f'-- RESULT for ({filePath}): {resultText}')
            except IOError:
                print(f'Unable to read in output image: {filePath}')
                continue

if __name__ == '__main__':
    main()
