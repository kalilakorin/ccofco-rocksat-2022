#!/usr/bin/env python

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

input_func = None
try:
    input_func = raw_input
except NameError:
    input_func = input


def confirm():
    i = ""
    while i not in ["y", "n"]:
        i = input_func("\n\r Okay to write values? [Y/N] ").lower()
    return i == "y"


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


def delay(timeAmount):  # enter delay time in ms
    time.sleep(timeAmount / 1000.0)  # div by 1000 since the sleep command is in seconds


def Qcommand(address):
    print(": Query tinyLiDAR Configuration Parameters ")
    (count, data) = pi.bb_i2c_zip(tlv.SDA,
                                  [_addr, address, _start, _write, 1, 0x51, _stop, _start, _read, 23, _stop, _end])
    try:
        return (count, data)
    except IndexError:
        print(" error in returned data! ")
        return 0
    delay(rebootTime)


def ContinuousReadingForTerminal(address):
    writeCommand(address, "MC")  # first set to continuous mode
    delay(3 * tlv.rebootTime)  # wait for reboot

    while True:
        delay(13)
        i = Read_Distance(address)
        sys.stdout.write(u"\u001b[100D " + str(i) + "mm    ")
        sys.stdout.flush()

        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            line = raw_input()
            printMenu()
            break

    writeCommand(address, "MS")  # set to SS mode
    delay(3 * tlv.rebootTime)  # wait for reboot

    printMenu()


def writeCommand2(address, command, dbyte):
    (count, data) = pi.bb_i2c_zip(tlv.SDA,
                                  [_addr, address, _start, _write, 1, command, _start, _write, 1, dbyte, _stop, _end])


def writeCommand(address, command):
    pi.exceptions = False
    if (len(command) == 2):
        (count, data) = pi.bb_i2c_zip(tlv.SDA,
                                      [_addr, address, _start, _write, 1, command[0], _start, _write, 1, command[1],
                                       _stop, _end])  # write 2 commands
    else:
        (count, data) = pi.bb_i2c_zip(tlv.SDA,
                                      [_addr, address, _start, _write, 1, command[0], _stop, _end])  # write 1 command


def Wcommand(address, param):
    (count, data) = pi.bb_i2c_zip(tlv.SDA,
                                  [_addr, address, _start, _write, 1, 0x57, _start, _write, 1, param[0], _start, _write,
                                   1, param[1], _start, _write, 1, param[2], _start, _write, 1, param[3], _start,
                                   _write, 1, param[4], _start, _write, 1, param[5], _stop, _end])


def CDcommand(address, offset):
    (count, data) = pi.bb_i2c_zip(tlv.SDA,
                                  [_addr, address, _start, _write, 1, "C", _start, _write, 1, "D", _start, _write, 1,
                                   offset[0], _start, _write, 1, offset[1], _stop, _end])  # write CD command


def CXcommand(address, offset):
    (count, data) = pi.bb_i2c_zip(tlv.SDA,
                                  [_addr, address, _start, _write, 1, "C", _start, _write, 1, "X", _start, _write, 1,
                                   offset[0], _start, _write, 1, offset[1], _stop, _end])  # write CX command


def Read_Distance(targetAddr):
    (count, data) = pi.bb_i2c_zip(tlv.SDA,
                                  [_addr, targetAddr, _start, _write, 1, "D", _stop, _start, _read, 2, _stop, _end])
    try:
        return data[0] * 256 + data[1]
    except IndexError:
        # print(" index error ")
        return 0


def Dcommand(numBytes, delayBetween, targetAddr):  # num of bytes, up to 255ms delay between and from targetAddr
    for i in range(0, numBytes):

        Measured_Distance = Read_Distance(targetAddr)

        if (Measured_Distance):
            print(u"\u001b[24A\u001b[100D\u001b[21B# Distance = %d mm\u001b[2A" % Measured_Distance)
        else:
            print(" - ")  # invalid distance data will show as '-'

        delay(delayBetween)


def printMenu():
    print(u"\u001b[2J\u001b[24A")
    print(u" \u001b[32;1m\
 tinyLiDAR Command Terminal BETA v0.95 for Raspberry Pi 3\u001b[0m ")
    print(u"\u001b[30;1m  Default I2C target address is 0x%X \u001b[0m " % tlv.I2C_Address)


def printMenu1():
    print(u"\
 \u001b[33;1md\u001b[0m - read distance                    \u001b[33;1mreset\u001b[0m - reset to factory defaults \n\r\
 \u001b[33;1mq\u001b[0m - query settings                   \u001b[33;1mw\u001b[0m - write custom VL53L0X config \n\r\
 \u001b[33;1mmc\u001b[0m - continuous mode                 \u001b[33;1mms\u001b[0m - single step mode \n\r\
 \u001b[33;1mpl\u001b[0m - long range preset               \u001b[33;1mps\u001b[0m - high speed preset \n\r\
 \u001b[33;1mph\u001b[0m - high accuracy preset            \u001b[33;1mpt\u001b[0m - tinyLiDAR preset \n\r\
 \u001b[33;1me\u001b[0m - disable LED indicator            \u001b[33;1mf\u001b[0m - enable LED indicator \n\r\
 \u001b[33;1mg\u001b[0m - LED on                           \u001b[33;1mt0\u001b[0m/\u001b[33;1mt1\u001b[0m - Disable/Enable WatchDogTimer\n\r\
 \u001b[33;1mcd\u001b[0m - cal offset distance             \u001b[33;1mcx\u001b[0m - cal crosstalk \n\r\
 \u001b[33;1mx\u001b[0m - reboot tinyLiDAR                 \u001b[33;1my\u001b[0m - save LED mode & reboot tinyLiDAR \n\r\
 \u001b[33;1mar\u001b[0mXX - auto I2C addr config loop     \u001b[33;1mv\u001b[0m - scan & verify I2C addr loop\n\r\
 \u001b[33;1mr\u001b[0mXX - change tinyLiDAR's I2C addr    \u001b[33;1mi\u001b[0mXX - change Terminal's I2C addr \n\r\
 \u001b[33;1mdc\u001b[0m - continuous read                 \
")
    print("> Please enter a command [XX = Hex I2C Addr, 'z' to Exit]")


print(stop_pigpio_daemon())  # stop pigpiod in case it was started already from a previous run
print(start_pigpio_daemon())  # start pigpiod now

pi = pigpio.pi()  # open local Pi
pi.bb_i2c_open(tlv.SDA, tlv.SCL, tlv.I2C_Speed)
