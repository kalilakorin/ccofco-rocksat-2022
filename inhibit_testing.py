# Skyler Puckett


import time
import RPi.GPIO as GPIO

rf = 6 # RF inhibit GPIO pin
am = 5 # arm motor inhibit GPIO pin

GPIO.setmode(GPIO.BCM)  #GPIO PIN NAMES
GPIO.setup (rf, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup (am, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

if GPIO.input (rf):
    print("rf wire connected")

if GPIO.input (rf):
    print("arm motor wire connected")