from open_gopro import GoPro

import gopromain as gopro
import time
import subprocess
import logging
import RPi.GPIO as GPIO

# test address D1:70:A4:FC:21:4F
# flight address E3:BB:1E:0D:C8:52

print("\nStart in Gopro...")
try:
    logger = logging.getLogger(__name__)
except:
    logger = None
    print('Unable to acquire the global logger object, assuming that gopro.py is being run on its own')

def main():
    # Configure & initialize the gopro to receive power from GPIO pins
    logging.info('Initializing GoPro RF test')

    gppower = 12  # GoPro power

    # GPIO pin assignment
    try:
        GPIO.setmode(GPIO.BCM)  # GPIO PIN NAMES
        GPIO.setup(gppower, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)  # power to the gopro camera
    except:
        logger.critical('Failed to initialize GPIO pins and GoPro for Wallops testing')
        return

    logger.info('Wallops RF test start: ' + str(int(time.time() * 1000)))

    # send power to the pin
    GPIO.output(gppower, GPIO.HIGH)

    # wait 15 seconds and turn off the pin
    time.sleep(15)
    GPIO.output(gppower, GPIO.LOW)

    # start the gopro
    subprocess.call(f'python3 gopromain.py --verbose -a "E3:BB:1E:0D:C8:52" -c "preset maxvideo" -c "record start"', shell=True)
    logger.info('GoPro record started: ' + str(int(time.time() * 1000)))
    time.sleep(5)
    subprocess.call(f'python3 gopromain.py --verbose -a "E3:BB:1E:0D:C8:52" -c "record stop"', shell=True)
    logger.info('GoPro record stopped: ' + str(int(time.time() * 1000)))

    GPIO.cleanup()

if __name__ == '__main__':
    main()

