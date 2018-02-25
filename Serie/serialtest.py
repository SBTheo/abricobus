import serial

port = serial.Serial("/dev/ttyS0", baudrate=9600)

while True:
    rcv = port.readline()
    print rcv