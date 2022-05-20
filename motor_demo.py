# Import modules
import time
import logging
import RPi.GPIO as GPIO
from adafruit_motorkit import MotorKit
import time




forward = 27 # Limit Switch Extension
stop = 22 # TE-2
reverse = 23 # Limit Switch Retraction
stop2 = 24 #second stop

# GPIO pin assignment

motor = MotorKit()
GPIO.setmode(GPIO.BCM)  #GPIO PIN NAMES
GPIO.setup (forward, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Forward
GPIO.setup (stop, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # STOP
GPIO.setup (reverse, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # REVERSE
GPIO.setup (stop2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # REVERSE

x= 1.0  # 5-RPM 0.55 throttle speed

while True:
    if GPIO.input(forward):
        print("Forward...\n")
        motor.motor1.throttle = x
        time.sleep(0.25)
    if GPIO.input(stop):
        print("Stop...\n")
        motor.motor1.throttle = 0.0
        time.sleep(0.25)
    if GPIO.input(reverse):
        print("Revers...\n")
        motor.motor1.throttle = -x
        time.sleep(0.25)
    if GPIO.input(stop2):
        print("Stop2...\n")
        motor.motor1.throttle = 0.0
        time.sleep(0.25)

    time.sleep(0.1)