import serial
import time
import RPi.GPIO as gp


port = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=.05)
gp.setmode(gp.BCM)
gp.setup(2,gp.OUT)
gp.setup(3,gp.OUT)
i = 0
while True:
    rcv = port.readline()
    lum = rcv.rstrip("\n")
    try:
        lum = float(lum.strip('\0'))
        print lum
        if lum < 1000:
            gp.output(2,gp.HIGH)
            gp.output(3,gp.HIGH)
        elif lum > 1000:
            gp.output(2,gp.LOW)
            gp.output(3,gp.LOW)
    except:
        pass
    if i == 500:
        port.write(b'10m@')
        i = 0
    i += 1
