from open_gopro import GoPro

import gopromain as gopro
import time
import subprocess

subprocess.call(f'python3 gopromain.py --verbose --address "D1:70:A4:FC:21:4F" --command "preset maxvideo" --command "record start"', shell=True)


#with GoPro() as gopro:
#    print("Yay! I'm connected via BLE, Wifi, initialized, and ready to send / get data now!")
    # Send some commands now

