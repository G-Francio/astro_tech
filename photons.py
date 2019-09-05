import numpy as np

# Costanti per i calcoli, a = angstrom
c = 2.99792e18 # a/s
h = 6.63e-27 # erg*s

# Dati specifici per banda
#  Visibile (555W): AB = 0.03, l = 5410 a, dl = 2789 a
#  Blu (438W): AB = 0.18, l = 4320 a, dl = 843 a

AB = 0.18
delta_l = 843
l = 4320

def photon_per_angstrom(AB_correction, l):
    flux_f = 10**(-(AB_correction + 48.6)/2.5)
    flux_l = c/l**2 * flux_f
    return flux_l * l/(h*c)

print('Fotoni per angstrm: %f' % photon_per_angstrom(AB, l))
print('Fotoni per filtro: %f' % (photon_per_angstrom(AB, l) * delta_l))
