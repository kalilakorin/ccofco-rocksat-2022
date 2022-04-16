# Import modules
import time
import logging
import RPi.GPIO as GPIO
from adafruit_motorkit import MotorKit



te1 = 27 # TE-1
forward = 22 # Limit Switch Extension
stop = 23 # TE-2
reverse = 24 # Limit Switch Retraction

# GPIO pin assignment

motor = MotorKit()
GPIO.setmode(GPIO.BCM)  #GPIO PIN NAMES
GPIO.setup (forward, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Forward
GPIO.setup (stop, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # STOP
GPIO.setup (reverse, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # REVERSE

while True:
    if GPIO.IN(forward):
        print("Forward...\n")
        motor.motor1.throttle = 1.0
    if GPIO.IN(stop):
        print("Stop...\n")
        motor.motor1.throttle = 0.0
    if GPIO.IN(reverse):
        print("Revers...\n")
        motor.moter1.throttle = -1.0
