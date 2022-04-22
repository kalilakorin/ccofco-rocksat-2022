# used to test the sent commands through the pi connected to a usb slot

#!/usr/bin/env python
import time
import serial


ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)
ser.close()
ser.open()

# def main():
while 1:
        x=ser.readline()
        print(str(x))


# if __name__ == '__main__':
#         main()
