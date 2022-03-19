from open_gopro import GoPro

import gopromain as gopro
import time
import subprocess
import RPi.GPIO as GPIO
import os

GPIO.setmode(GPIO.BCM)  #GPIO PIN NAMES
ter = 17
GPIO.setup(ter, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # TE-1 around +85 seconds

def main():
    while True:
        if GPIO.input(ter):
            break
    while True:
        btReturn = os.system(f'python3 gopromain.py --verbose -a "D1:70:A4:FC:21:4F" -c "preset maxvideo" -c "record start"')
        if 'Error' not in str(btReturn):
            break

if __name__ == '__main__':
    main()

#with GoPro() as gopro:
#    print("Yay! I'm connected via BLE, Wifi, initialized, and ready to send / get data now!")
    # Send some commands now
