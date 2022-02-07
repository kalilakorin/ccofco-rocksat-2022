
from time import sleep
import RPi.GPIO as GPIO

import time
from adafruit_motorkit import MotorKit

#motor = MotorKit()
pin1 = 27
pin2 = 22
pin3 = 23
pin4 = 24


GPIO.setmode(GPIO.BCM)  # Pin# not GPIO#
GPIO.setup(pin1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # TE-1 around +85 seconds  GPIO27 blue
GPIO.setup(pin2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Extension Limit Switch   GPIO22 yellow
GPIO.setup(pin3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # TE-2 around +220 seconds GPIO23 blue
GPIO.setup(pin4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Retraction Limit Switch  GPIO24 yellow
print("pin and motor initialized")
# wait for TE-1 signal
while True:
    if GPIO.input (pin1):
        break

#motor.motor1.throttle = 1.0
print ("TE-1 Detected...\n\n")
# wait for extension limit switch activation
while True:
    if GPIO.input (pin2):
        break

#motor.motor1.throttle = 0
print ("Extension Stop Detected...\n\n")
# wait for TE-2 signal
while True :
    if GPIO.input (pin3):
        break

#motor.motor1.throttle = -.75
print ("TE-2 Detected...\n\n")
# wait for retraction limit switch activation
while True :
    if GPIO.input (pin4):
        break

#motor.motor1.throttle = 0
print ("Retraction Stop Detected...\n\n")

GPIO.cleanup ()

