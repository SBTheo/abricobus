import serial
import Adafruit_DHT
import datetime
import time
import RPi.GPIO as gp
from threading import Thread


class Temperature(Thread):
    def __init__(self,
                 pin_int="",
                 pin_ext="",
                 pin_rad=""):
        Thread.__init__(self)
        self.pin_int = pin_int
        self.pin_ext = pin_ext
        self.pin_rad = pin_rad
        self.temp_int = -1
        self.temp_ext = -1
        self.etat_rad = 0
        self.stop = 0
        gp.setmode(gp.BCM)
        gp.setwarnings(False)
        gp.setup(int(self.pin_rad), gp.OUT)
        gp.output(int(self.pin_rad), gp.LOW)
        self.port = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=.05)

    def abs(self, a):
        if a < 0:
            return -a
        else:
            return a

    def setStop(self):
        self.stop = 1

    def getint(self):
        try:
            humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, self.pin_int)
            temp = '{0:0.3f}'.format(temperature)
            self.temp_int = float(temp)
            return 1
        except:
            return -1

    def getext(self):
        try:
            humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, self.pin_ext)
            temp = '{0:0.3f}'.format(temperature)
            #print '{1:0.1f}%' % (humidity)
            self.temp_ext = float(temp)
            return 1
        except:
            return -1

    def get_temp_int(self):
        return self.temp_int

    def get_temp_ext(self):
        return self.temp_ext

    def get_etat_rad(self):
        return self.etat_rad

    def set_pin_int(self, pin=""):
        self.pin_int = pin

    def set_pin_ext(self, pin=""):
        self.pin_ext = pin

    def radiateur(self):
        self.getext()
        self.getint()
        if self.etat_rad == 0 and self.temp_ext < 30 and \
                (datetime.datetime.now().hour > 7 and datetime.datetime.now().hour < 21):
            self.etat_rad = 1
            gp.output(int(self.pin_rad), gp.HIGH)
            print "rad on"
        elif self.temp_ext > 30 or self.temp_int > self.temp_ext or (datetime.datetime.now().hour < 7 and datetime.datetime.now().hour > 21):
            self.etat_rad = 0
            gp.output(int(self.pin_rad), gp.LOW)
            print "rad off"


    def run(self):
        while True:
            self.radiateur()
            time.sleep(15)
            s = 'TT=_%dC@' % (self.temp_ext)
            self.port.write(b'{0}'.format(s))
            if self.stop == 1:
                break
        print "fin temperature"
