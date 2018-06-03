import sys
import os
sys.path.append(os.getcwd())
import abri.temperature as temperature
import abri.bus as bus
import abri.lumiere as lumiere
import time

if __name__ == "__main__":
    t = temperature.Temperature(pin_int="17",
                   pin_ext="18",
                   pin_rad="2")
    b = bus.Bus()
    l = lumiere.Lumiere(pin_mouv=7,
                pin_rel=3,
                niveau=1900)
    try:
        t.start()
        b.start()
        l.start()
        
        #t.join()
        #b.join()
        #l.join()
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        t.setStop()
        b.setStop()
        l.setStop()
        print "Quit"
        sys.exit(0)
