# Astronomical_Techniques

Script utilizzati per le simulazioni. Richiedono [Python3](https://www.python.it/), [MatPlotLib](https://matplotlib.org/) e [Scipy](https://matplotlib.org/), assieme ai file .txt che contengono i dati testuali che vengono importanti negli script (F555W.txt, F438W, earthshine.txt, zodiacal_light.txt, V_21Mag.txt, B_21Mag.txt, King_profile.txt).

Ogni script effettua una parte dell'analisi in modo differente:
 - distribution.py: si occupa di simulare la distribuzione di oggetti e stimare la regione in cui non vengono risolti singolarmente
 - bisezioneSNR_XBand.py: calcola il tempo necessario per ottenere il segnale rumore desiderato in banda X, usando tutte le approssimazioni possibili (efficienza media, fotoni a priori)
 - efficiency_interpolation.py: calcola l'efficienza media per il sistema telescopio/filtri
 - photons.py: calcola il fattore n_0 nella formula usata per il flusso di fotoni per le varie sorgenti
 - X_bisezioneSNR_integral.py: calcola il tempo necessario per ottenere il segnale rumore desiderato in banda X, cercando di usare gli spetti effettivi del cielo e della sorgente
