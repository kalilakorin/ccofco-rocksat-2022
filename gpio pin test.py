
from time import sleep
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BOARD)  # Pin# not GPIO#
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # TE-1 around +85 seconds
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Extension Limit Switch
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # TE-2 around +220 seconds
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Retraction Limit Switch




while True:
    if GPIO.input(13):
        print("TE-1: " + str(GPIO.input(13)))

    else:
        print("...")

    if GPIO.input(15):
        print("Extension Limit Switch detected")
    else:
        print("...")
    if GPIO.input(16):
        print("TE-2 detected")
    else:
        print("...")

    if GPIO.input(18):
        print("Retraction Limit Switch detected")
    else:
        print("...")
    sleep(3)