# Skyler Puckett
#
# ffmpeg -t "01:00" -y -video_size 1280x720 -framerate 60 -i /dev/video0 -f flv test.flv
# ffmpeg -f v4l2 -video_size 1280x720 -i /dev/video0 -frames 1 out.jpg

import subprocess
import logging
# import RPi.GPIO as GPIO
# from time import sleep

try:
    logger = logging.getLogger(__name__)
except:
    logger = None
    print('Unable to acquire the global logger object, assuming that auxcam.py is being run on its own')

def main():
    # pin3 = 23
    # GPIO.setmode(GPIO.BCM)
    # GPIO.setup(pin3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # TE-2 around +220 seconds GPIO23 blue
    logging.info('USB-camera: Recording Started...')

    for vidNo in range(0, 15):
        subprocess.call(f'ffmpeg -t "00:30" -y -video_size 1280x720 -framerate 60 -i /dev/video0 -f flv test{str(vidNo)}.flv', shell=True)

    logging.info('USB-camera: Recording Stopped...')
    # print("stop soon")
    # while True:
    #     if GPIO.input(pin3):
    #         break
    #
    # sleep(10)
    # subprocess.call('signal.SIGINT', shell=True)

if __name__ == '__main__':
    main()