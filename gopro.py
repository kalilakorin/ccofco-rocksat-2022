from open_gopro import GoPro

import gopromain as gopro
import time
import subprocess
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)  #GPIO PIN NAMES

GPIO.setup(ter, 17, pull_up_down=GPIO.PUD_DOWN)  # TE-1 around +85 seconds

while True:
    if GPIO.input(ter):
        break
subprocess.call(f'python3 gopromain.py --verbose -a "D1:70:A4:FC:21:4F" -c "preset maxvideo" -c "record start"', shell=True)


#with GoPro() as gopro:
#    print("Yay! I'm connected via BLE, Wifi, initialized, and ready to send / get data now!")
    # Send some commands now
