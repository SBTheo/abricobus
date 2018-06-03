import serial
import RPi.GPIO as gp
import time
import datetime
from threading import Thread


class Lumiere(Thread):

    def __init__(self,
                 pin_mouv=0,
                 pin_rel=0,
                 niveau=0):
        self.etat = 0
        self.presence = 0
        self.port = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=.05)
        self.pin_mouv = pin_mouv
        self.pin_rel = pin_rel
        self.niveau = niveau
        self.stop = 0
        gp.setmode(gp.BCM)
        gp.setwarnings(False)
        gp.setup(int(self.pin_mouv), gp.IN)
        gp.setup(int(self.pin_rel), gp.OUT)
        gp.output(self.pin_rel, gp.LOW)
        Thread.__init__(self)

    def setStop(self):
        self.stop = 1

    def get_etat(self):
        return self.etat

    def get_presence(self):
        return self.presence

    def get_lum(self):
        return self.lum

    def read_lum(self):
        try:
            rcv = self.port.readline()
            lum = rcv.rstrip("\n")
            lum = lum.strip('\0')
            lum = float(lum)
            #print lum
            return lum
        except:
            return -1

    def lum_int(self):
        lum = self.read_lum()
        self.presence = gp.input(int(self.pin_mouv))
        #print self.presence, datetime.datetime.now().hour, self.niveau
        if (datetime.datetime.now().hour > 7 and datetime.datetime.now().hour < 21) and \
            lum < self.niveau and \
            self.presence == 1 and \
            self.etat == 0:
            gp.output(self.pin_rel, gp.HIGH)
            self.etat = 1
            time.sleep(20)
            print "lumiere on"
        elif (datetime.datetime.now().hour < 7 and datetime.datetime.now().hour > 21) or \
            lum > self.niveau or self.presence == 0:
            self.etat = 0
            gp.output(self.pin_rel, gp.LOW)
            #print "lumiere off"

    def run(self):
        while 1:
            self.lum_int()
            #time.sleep(1)
            
            if self.stop == 1:
                break
        print "fin lumiere"
