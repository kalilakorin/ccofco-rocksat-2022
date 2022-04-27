from open_gopro import GoPro

import gopromain as gopro
import time
import subprocess

# test address D1:70:A4:FC:21:4F
# flight address E3:BB:1E:0D:C8:52

subprocess.call(f'python3 gopromain.py --verbose -a "E3:BB:1E:0D:C8:52" -c "preset maxvideo" -c "record start"', shell=True)


#with GoPro() as gopro:
#    print("Yay! I'm connected via BLE, Wifi, initialized, and ready to send / get data now!")
    # Send some commands now
