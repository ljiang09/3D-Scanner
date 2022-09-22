"""
"""

import serial

arduinoComPort = "/dev/ttyACM0"
baud_rate = 9600
serialPort = serial.Serial(arduinoComPort, baud_rate, timeout=10)

while True:
  lineOfData = serialPort.readline().decode()
  if len(lineOfData) > 0:
    read_to_volt = lineOfData
    print(read_to_volt)
