from scipy.interpolate import make_interp_spline, BSpline
from scipy.integrate import quad
import numpy as np

# Costanti per i calcoli, a = angstrom
c = 2.99792e18 # a/s
h = 6.626070e-27   # erg*s

def sr(t_exp):
    signal_photon = flux_star * A * t_exp
    bkg_photon = flux_bkg * delta * A * t_exp
    dark_photon = DK * delta/p**2 * t_exp
    RON_photon = RON**2 * delta/p**2

    print('Fotoni corrispondenti alle varie sorgenti: \n - segnale: %f \n - background: %f \n \
- dark: %f \n - RON: %f \n - Bkg (no delta): %f, \n - Dark (no t_exp): %f, \n - F. di fotoni (sorgente): %f'
% (signal_photon, bkg_photon,dark_photon, RON_photon, bkg_photon/delta, dark_photon/t_exp, flux_star))

    N = np.sqrt(signal_photon + RON_photon + bkg_photon + dark_photon)
    SNR = signal_photon/N
    print('\nSegnale rumore per la misura: %f \n' % SNR)

    return SNR

# * ---------------------------------------  **  --------------------------------------- * #

# I parametri cambiano da filtro a filtro! Controlla tutto 8 volte almeno!
# Fai riferimento a: http://etc.stsci.edu/etcstatic/users_guide/1_ref_9_background.html

FWHM = 0.2 #
prim_diam = 240 # In centimetri - !! Non sono del tutto sicuro !!
sec_diam = 30 # In centimetri - !! Non sono del tutto sicuro !!
eta = 0.224 # Ricavato tramite interpolazione e media integrale
t_exp = 34.217 # Questo sara' comunque trovato per bisezione
DK = 0.0023 # Indicati: 9 e- per ora per pixel - preso dal sito della simulazione
p = 0.0395 #
RON = 3.1 #
# Per lui ^ ci sono due valori, uno da: http://etc.stsci.edu/etcstatic/users_guide/1_ref_9_background.html
#  e uno da: https://hst-docs.stsci.edu/display/WFC3IHB/5.1+Overview+of+this+Chapter#id-5.1OverviewofthisChapter-table1

# * ---------------------------------------  **  --------------------------------------- * #

# Calcolo delle quantita' che non richiedono di essere ricalcolate ad ogni passaggio
A_prim = (prim_diam/2.) ** 2 * np.pi
A_sec = (sec_diam/2.) ** 2 * np.pi
A = A_prim - A_sec
delta = np.pi * FWHM**2 # Questo in realta' e' delta^2
# flux_star = 1  flux(magnitude) <-- sostituito dal codice sotto
# flux_bkg = flux(magnitude_sky) # Questo e' da aggiornare per le luci zodiacali.

# * ---------------------------------------  **  --------------------------------------- * #

# Interpolazione delle efficienze e tentativo di integrazione

# Limiti di integrazione
start = 2500
stop = 8000

# Andamento del passabanda
x_passband, y_passband = [], []
with open('F555W.txt') as f:
    for line in f:
        new_line = line.split(' ')
        x_passband.append(float(new_line[0]))
        y_passband.append(float(new_line[1].rstrip()))
f.close()
spl_bandpass = make_interp_spline(x_passband, y_passband, k = 3) # funzione per interpolare il passabanda

# Andamento del flusso dell'oggetto - grafico del sito. Nota che corrisponde a flux_l
x_filter, y_filter = [], []
with open('V_21mag.txt') as f:
    for line in f:
        new_line = line.split(' ')
        x_filter.append(float(new_line[0]))
        y_filter.append(float(new_line[1].rstrip()))
f.close()
spl_flux = make_interp_spline(x_filter, y_filter, k = 3) # funzione per interpolare il flusso dell'oggetto

# Earthshine
x_earthshine, y_earthshine = [], []
with open('earthshine.txt') as f:
    for line in f:
        new_line = line.split(' ')
        x_earthshine.append(float(new_line[0]))
        y_earthshine.append(float(new_line[1].rstrip()))
f.close()
spl_earthshine = make_interp_spline(x_earthshine, y_earthshine, k = 3)

# Luci Zodiacali
x_zodiacal, y_zodiacal = [], []
with open('zodiacal_light.txt') as f:
    for line in f:
        new_line = line.split(' ')
        x_zodiacal.append(float(new_line[0]))
        y_zodiacal.append(float(new_line[1].rstrip()))
f.close()
spl_zodiacal = make_interp_spline(x_zodiacal, y_zodiacal, k = 3)

def photon_per_angstrom(flux_l, l):
    return flux_l(l) * l/(h*c)

def product_signal(l):
    return photon_per_angstrom(spl_flux, l) * spl_bandpass(l) # Dovrebbe ritornare il prodotto flusso*efficienza,
                                                              #  in funzione di lambda
def product_bkg(l):
    return (photon_per_angstrom(spl_earthshine, l) + photon_per_angstrom(spl_zodiacal, l)) * spl_bandpass(l)

x_tot = x_filter.extend((x_zodiacal + x_earthshine + x_passband))

flux_star = quad(product_signal, start, stop, points = x_filter, limit = len(x_filter))[0]
flux_bkg = quad(product_bkg, start, stop, points = x_filter, limit = len(x_filter))[0]

# * ---------------------------------------  **  --------------------------------------- * #

# Codice di bisezione

target_sr = 50
tol = 0.0000001*target_sr
up = 100000
down = 0
t_exp = (up + down)/2

while abs(sr(t_exp) - target_sr) > tol:
    t_exp = (up + down)/2
    if sr(t_exp) > target_sr:
        up = t_exp
    else:
        down = t_exp

print("Il tempo di esposizione necessario per un snr di %f e' %f" % (sr(t_exp), t_exp))
