# Skyler Puckett
#
# ffmpeg -t "01:00" -y -video_size 1280x720 -framerate 60 -i /dev/video0 -f flv test.flv
# ffmpeg -f v4l2 -video_size 1280x720 -i /dev/video0 -frames 1 out.jpg

import subprocess
import RPi.GPIO as GPIO
from time import sleep



def main():
    # pin3 = 23
    # GPIO.setmode(GPIO.BCM)
    # GPIO.setup(pin3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # TE-2 around +220 seconds GPIO23 blue

    subprocess.call(['ffmpeg', '-t "01:00" -y -video_size 1280x720 -framerate 60 -i /dev/video0 -f flv test.flv'])

    # subprocess.call('ffmpeg -t "07:25" -y -video_size 1280x720 -framerate 60 -i /dev/video0 -f flv test.flv', shell=True)
    # print("stop soon")
    # while True:
    #     if GPIO.input(pin3):
    #         break
    #
    sleep(10)
    subprocess.call('signal.SIGINT', shell=True)

if __name__ == '__main__':
    main()
