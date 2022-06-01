import os
import time

from goprocam import GoProCamera, constants
gpCam = GoProCamera.GoPro()

deletepath = '/home/pi/Documents/gopro-ble-py-2'
homepath = '/home/pi/ccofco-rocksat-2022'

print("Current working directory: {0}".format(cwd))
time.sleep(2)
os.chdir(deletepath)
print("Changed to directory: {0}".format(cwd))
time.sleep(2)
os.chdir(homepath)
print("Changed to directory: {0}".format(cwd))


## Downloads all of the SD card's contents and then formats the sd card.

# gpCam.downloadAll()
# gpCam.delete("all")