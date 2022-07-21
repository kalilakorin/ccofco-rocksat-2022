from open_gopro import GoPro

import gopromain as gopro
import time
import subprocess
import logging

# test address D1:70:A4:FC:21:4F
# OLD flight address E3:BB:1E:0D:C8:52
# NEW flight address DF:C9:00:93:B7:8D

print('\nInitializing GoPro RF test')
try:
    logger = logging.getLogger(__name__)
except:
    logger = None
    print('Unable to acquire the global logger object, assuming that gopro.py is being run on its own')

def main():
    # Configure & initialize the gopro to receive power from GPIO pins
    logger.info('Wallops RF test start: ' + str(int(time.time() * 1000)))

    # wait 15 seconds to allow camera to turn on
    time.sleep(15)

    # start the gopro
    for x in range(0, 3):
        subprocess.call(f'python3 gopromain.py --verbose -a "DF:C9:00:93:B7:8D" -c "record start"', shell=True)
        logger.info('GoPro test record started: ' + str(int(time.time() * 1000)) + '\n')
        time.sleep(5)
    for x in range(0, 3):
        subprocess.call(f'python3 gopromain.py --verbose -a "DF:C9:00:93:B7:8D" -c "record stop"', shell=True)
        logger.info('GoPro test record stopped: ' + str(int(time.time() * 1000)) + '\n')
        time.sleep(5)
    for x in range(0, 3):
        subprocess.call(f'python3 gopromain.py --verbose -a "DF:C9:00:93:B7:8D" -c "poweroff"', shell=True)
        logger.info('GoPro test power off: ' + str(int(time.time() * 1000)) + '\n')
        time.sleep(5)

if __name__ == '__main__':
    main()