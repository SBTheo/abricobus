"""importation des codes pour les differents capteurs""""
import sys
import os
sys.path.append(os.getcwd())
import temperature
import bus
import lumiere
"""declaration des pins pour la temperature"""
t = temperature.Temperature(pin_int="17",
                pin_ext="18",
                pin_rad="2")
b = bus.Bus()
"""declaration des pins pour la lumiere"""
l = lumiere.Lumiere(pin_mouv="7",
            pin_rel="3",
            niveau=1000)
t.start()
b.start()
l.start()

t.join()
b.join()
l.join()