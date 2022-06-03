# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Carter Nelson for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

# Simple demo of the VL53L1X distance sensor.
# Will print the sensed range/distance every second.

# import time
# import board
# import adafruit_vl53l1x
#
# i2c = board.I2C()
#
# vl53 = adafruit_vl53l1x.VL53L1X(i2c)
#
# # OPTIONAL: can set non-default values
# vl53.distance_mode = 1
# vl53.timing_budget = 100
#
# print("VL53L1X Simple Test.")
# print("--------------------")
# model_id, module_type, mask_rev = vl53.model_info
# print("Model ID: 0x{:0X}".format(model_id))
# print("Module Type: 0x{:0X}".format(module_type))
# print("Mask Revision: 0x{:0X}".format(mask_rev))
# print("Distance Mode: ", end="")
# if vl53.distance_mode == 1:
#     print("SHORT")
# elif vl53.distance_mode == 2:
#     print("LONG")
# else:
#     print("UNKNOWN")
# print("Timing Budget: {}".format(vl53.timing_budget))
# print("--------------------")
#
# vl53.start_ranging()
#
# while True:
#     if vl53.data_ready:
#         print("Distance: {} cm".format(vl53.distance))
#         vl53.clear_interrupt()
#         time.sleep(1.0)

from subprocess import Popen, PIPE
import sys, select, time
import pigpio  # http://abyz.me.uk/rpi/pigpio/python.html
import tl_variables as tlv

# pigpio bitbang i2c states
_addr = 4
_start = 2
_stop = 3
_end = 0
_write = 7
_read = 6
# -------------------------

def start_pigpio_daemon():
    p = Popen("sudo pigpiod", stdout=PIPE, stderr=PIPE, shell=True)

    s_out = p.stdout.readline()
    s_err = p.stderr.readline()

    if s_out == '' and s_err == '':
        return 0  # started OK
    elif "pigpio.pid" in s_err:
        print('Error 1')
        return 1  # already started
    else:
        print('Error!')
        return 2  # error


def stop_pigpio_daemon():
    p = Popen("sudo killall pigpiod", stdout=PIPE, stderr=PIPE, shell=True)

    s_out = p.stdout.readline()
    s_err = p.stderr.readline()

    if s_out == '' and s_err == '':
        return 0  # killed OK
    else:
        return 2  # error

if __name__ == '__main__':
    print(stop_pigpio_daemon())  # stop pigpiod in case it was started already from a previous run
    print(start_pigpio_daemon())  # start pigpiod now

    pi = pigpio.pi()  # open local Pi
    pi.bb_i2c_open(tlv.SDA, tlv.SCL, tlv.I2C_Speed)