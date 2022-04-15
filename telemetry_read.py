# used to test the sent commands through the pi connected to a usb slot

#!/usr/bin/env python
import time
import serial


ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)
def main():
        while 1:
                x=ser.read(2)
                print(x)

if __name__ == '__main__':
        main()
