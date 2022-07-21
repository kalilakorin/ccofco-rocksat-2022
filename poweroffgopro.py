#from open_gopro import GoPro

import gopromain as gopro
import time
import subprocess
import logging

# test address D1:70:A4:FC:21:4F
# OLD flight address E3:BB:1E:0D:C8:52
# NEW flight address DF:C9:00:93:B7:8D

print("In power off GoPro...\n")
try:
    logger = logging.getLogger(__name__)
except:
    logger = None
    print('Unable to acquire the global logger object, assuming that poweroffgopro.py is being run on its own.\n')

def main():
    # Configure & initialize the gopro to receive power from GPIO pins
    logging.info('Initializing GoPro')
    subprocess.call(f'python3 gopromain.py --verbose -a "DF:C9:00:93:B7:8D" -c "poweroff"', shell=True)
    logger.info('GoPro power off: ' + str(int(time.time() * 1000)) + '\n')

if __name__ == '__main__':
    main()