import serial
import time
import RPi.GPIO as gp
from threading import Thread


class Bus(Thread):
    def __init__(self):
        self.port = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=.05)
        self.stop = 0
        #g11, g12, a1 ,b1, c1, d1, g21, g22, a2, b2, c2, d2, g31, g32, a3, b3, c3, d3
        self.pins = [11, 22, 9, 10, 27, 4, 21, 13, 26, 19, 6, 5, 25, 12, 24, 23, 16, 20]
        #etats du chenillard
        #self.etats = [199728,32768,16384,49152,131072,139264,135168,143360,196608,197120,196864,197376,198656,198784,198720,198848,199680,199688,199684,199692,199712,199714,199713,199715,199728]
        self.etats = [68656, 101424, 85040, 117808, 134192, 142384, 138288, 146480, 197680, 198192, 197936, 198448, 198704, 198832, 198768, 198896, 199696, 199704, 199700, 199708, 199712, 199714, 199713, 199715, 199728]

        for i in self.pins:
            gp.setup(i, gp.OUT)

        gp.setmode(gp.BCM)
        gp.setwarnings(False)
        gp.setup(11, gp.OUT)
        gp.setup(9, gp.OUT)
        gp.setup(10, gp.OUT)
        Thread.__init__(self)

    def chenillard(self, indice=0):
        etat = "{0:018b}".format(self.etats[indice])
        for i in range(0,18):
            gp.output(self.pins[i], int(etat[i]))

    def setStop(self):
        self.stop = 1
    
    def run(self):
        compte = 0
        indice = 0
        gp.output(11, gp.LOW)
        gp.output(9, gp.HIGH)
        gp.output(10, gp.HIGH)
        while True:
            s = '%dm@' % (30-compte)
            self.port.write(b'{0}'.format(s))
            time.sleep(15)
            self.chenillard(indice=indice)
            if indice < 24:
                indice += 1
            else:
                indice = 0
            if compte < 30:
                compte += 5
            else:
                compte = 0
            if self.stop == 1:
                break
        print "fin bus"
