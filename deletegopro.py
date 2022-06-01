import os
import time

from goprocam import GoProCamera, constants
gpCam = GoProCamera.GoPro()

deletepath = '/home/pi/Documents/gopro-py-api-master'
homepath = '/home/pi/ccofco-rocksat-2022'

print("Current working directory: {0}".format(os.getcwd()))
time.sleep(2)
os.chdir(deletepath)
print("Changed to directory: {0}".format(os.getcwd()))
gpCam.delete("all")
time.sleep(20)
os.chdir(homepath)
print("Changed to directory: {0}".format(os.getcwd()))


## Downloads all of the SD card's contents and then formats the sd card.

# gpCam.downloadAll()
# gpCam.delete("all")