import math as m

def flux(num):
    N_0 = 905379
    return_flux = N_0 * 10**(-0.4*num)
    return return_flux

def sr(t_exp):
    A_primary = (prim_diam/2.) ** 2 * m.pi
    A_secondary = (sec_diam/2.) ** 2 * m.pi
    A = A_primary - A_secondary
    delta = m.pi * FWHM**2 # Questo in realta' e' delta^2

    flux_star = flux(magnitude)
    flux_bkg = flux(magnitude_sky)

    signal_photon = flux_star * A * eta * t_exp
    bkg_photon = flux_bkg * delta * A * eta * t_exp
    dark_photon = DK * delta/p**2 * t_exp
    RON_photon = RON**2 * delta/p**2

    print('Fotoni corrispondenti alle varie sorgenti: \n - segnale: %f \n - background: %f \n \
- dark: %f \n - RON: %f \n - Bkg (no delta): %f, \n - Dark (no t_exp): %f, \n - F. di fotoni (sorgente): %f'
% (signal_photon, bkg_photon,dark_photon, RON_photon, bkg_photon/delta, dark_photon/t_exp, flux_star))

    N = m.sqrt(signal_photon + RON_photon + bkg_photon + dark_photon)
    SNR = signal_photon/N
    print('\nSegnale rumore per la misura: %f \n' % SNR)

    return SNR


magnitude = 21 #
magnitude_sky = 23.2 # High da quanto dice il sito

prim_diam = 240 # In centimetri - !! Non sono del tutto sicuro !!
sec_diam = 30 # In centimetri - !! Non sono del tutto sicuro !!
eta = 0.181 # Ricavato tramite interpolazione e media integrale
t_exp = 30 # Questo sara' comunque trovato per bisezione
DK = 0.0023 #
p = 0.0395 #
RON = 3.1 #

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

print('Il tempo di esposizione necessario per un snr di %f è %f' % (sr(t_exp), t_exp))
# print(signal_photon, RON_photon, sky_photon)
