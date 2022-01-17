

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)  # Pin# not GPIO#
GPIO.setup(13, GPIO.IN)  # TE-1 around +85 seconds
GPIO.setup(15, GPIO.IN)  # Extension Limit Switch
GPIO.setup(16, GPIO.IN)  # TE-2 around +220 seconds
GPIO.setup(18, GPIO.IN)  # Retraction Limit Switch

while True:
    if GPIO.input(13):
        print("TE-1 detected")
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
    sleep(1)