#from open_gopro import GoPro

import gopromain as gopro
import time
import subprocess
import logging

# test address D1:70:A4:FC:21:4F
# flight address E3:BB:1E:0D:C8:52

print("Start in Gopro...\n")
try:
    logger = logging.getLogger(__name__)
except:
    logger = None
    print('Unable to acquire the global logger object, assuming that gopro.py is being run on its own.\n')

def main():
    # Configure & initialize the gopro to receive power from GPIO pins
    logging.info('Initializing GoPro')

    while True:
        # wait 15 seconds and turn off the pin
        time.sleep(15)
        # start the gopro
        subprocess.call(f'python3 gopromain.py --verbose -a "D1:70:A4:FC:21:4F" -c "preset maxvideo" -c "record start"', shell=True)
        logger.info('GoPro record started: ' + str(int(time.time() * 1000)) + '\n')

if __name__ == '__main__':
    main()