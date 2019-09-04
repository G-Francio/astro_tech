import math as m

def flux(num):
    N_0 = 2746235
    return_flux = N_0 * 10**(-0.4*num)
    return return_flux

def sr(t_exp):
    A_primary = (prim_diam/2.) ** 2 * m.pi
    A_secondary = (sec_diam/2.) ** 2 * m.pi
    A = A_primary - A_secondary
    delta = m.pi * FWHM**2 # Questo in realta' e' delta^2

    flux_star = flux(magnitude)
    flux_bkg = flux(magnitude_sky) # Questo e' da aggiornare per le luci zodiacali.

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

# valido per hst, e non so nemmeno quanto! Controlla tutto 6 volte almeno!

# I parametri cambiano da filtro a filtro! Controlla tutto 8 volte almeno!
# Fai riferimento a: http://etc.stsci.edu/etcstatic/users_guide/1_ref_9_background.html

magnitude = 21 #
magnitude_sky = 22.1 # high da quanto dice il sito, unico valore che non torna
FWHM = 0.2 #
prim_diam = 240 # In centimetri - !! Non sono del tutto sicuro !!
sec_diam = 30 # In centimetri - !! Non sono del tutto sicuro !!
eta = 0.163 # Ricavato tramite interpolazione e media integrale
t_exp = 34.217 # Questo sara' comunque trovato per bisezione
DK = 0.0023 # Indicati: 9 e- per ora per pixel - preso dal sito della simulazione
p = 0.0395 #
RON = 3.1 #
# Per lui ^ ci sono due valori, uno da: http://etc.stsci.edu/etcstatic/users_guide/1_ref_9_background.html
#  e uno da: https://hst-docs.stsci.edu/display/WFC3IHB/5.1+Overview+of+this+Chapter#id-5.1OverviewofthisChapter-table1

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
