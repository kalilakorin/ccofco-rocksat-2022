import serial
ser = serial.Serial("COM3", 9600)
while True:
     cc=str(ser.readline())
     print(cc)