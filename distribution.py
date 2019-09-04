import matplotlib.pyplot as plt
import scipy.interpolate
import random as r
import scipy as sp
import numpy as np

import time as t

def log_interp1d(xx, yy, kind='linear'):
    # Interpola meglio la funzione
    '''funzione di interpolazione del profilo di king'''
    logx = np.log10(xx)
    logy = np.log10(yy)
    lin_interp = sp.interpolate.interp1d(logx, logy, kind=kind)
    log_interp = lambda zz: np.power(10.0, lin_interp(np.log10(zz)))
    return log_interp

def rescale(number, max_old, min_new, max_new):
    # Riscala numeri casuali tra 0  e N nell'intervallo che ti serve
    return min_new + 2*number*max_new/max_old

def all_coordinates(cell_dictionary):
    # Ritorna le coordinate (x, y) degli oggetti in **arcominuti**
    x, y = [], []
    for key in cell_dictionary:
        single_cell_coordinates = cell_dictionary[key].cluster_coordinates()
        for tup in single_cell_coordinates:
            x.append(tup[0])
            y.append(tup[1])
    return (x, y)

def distance(tup_i, tup_j):
    # Ritorna la distanza tra due stelle
    return np.sqrt((tup_i[0]-tup_j[0])**2 + (tup_i[1]-tup_j[1])**2)

def arcsec_to_arcmin(arcsec):
    return 1/60*arcsec

def arcmin_to_arcsec(arcmin):
    return 60*arcmin

def close_stars(star_coordinates, threshold = arcsec_to_arcmin(0.2)):
    # Funzione da semplificare perchè di sicuro si può trovare un algoritmo intelligente
    # A prescindere, credo funzionerà solo per aperture circolari

    check_list, x, y = [], [], []
    star_number = len(star_coordinates[0])
    
    for i in range(star_number):
        for j in range(i+1, star_number):
            star_coord_one = (star_coordinates[0][i], star_coordinates[1][i])
            star_coord_two = (star_coordinates[0][j], star_coordinates[1][j])
            star_distance = distance(star_coord_one, star_coord_two)
            if star_distance < threshold:
                if star_coord_one not in check_list:
                    check_list.append(star_coord_one)
                    x.append(star_coord_one[0])
                    y.append(star_coord_one[1])
                if star_coord_two not in check_list:
                    check_list.append(star_coord_two)
                    x.append(star_coord_two[0])
                    y.append(star_coord_two[1])
    return (x, y)

def plot_something(tup, size, color, scatter = True):
    # Plotta la distribuzione di oggetti
    x, y = [], []
    for (i, j) in zip(tup[0], tup[1]):
        x.append(i)
        y.append(j)

    if scatter:
        plt.scatter(x, y, s = size, c = color)
    else:
        plt.plot(x, y, s = size, c = color)

# * -------------------------------------- ** -------------------------------------- * #

x_interpolation, y_interpolation = [], []

with open('king_profile.txt') as f:
    for line in f:
        new_line = line.split(' ')
        x_interpolation.append(float(new_line[0]))
        y_interpolation.append(float(new_line[1].rstrip()))
f.close()
interpolation_function = log_interp1d(x_interpolation, y_interpolation, kind = 'cubic')

def object_number_function(distance):
    return interpolation_function(distance)

# * -------------------------------------- ** -------------------------------------- * #

class cell:
    max_rand = 1000
    
    # Importante: side è un float, center position è una tupla, object position una lista di tuple
    def __init__(self, side, cell_center, cell_index):
        self.side = side
        self.cell_center = cell_center
        self.cell_index = cell_index
        self.local_coordinates = []
        self.global_coordinates = []

    # Ritorna l'area della cella
    def area(self):
        return self.side**2

    # Ritorna la distanza dal centro delle coordinate
    def distance_to_center(self):
        return np.sqrt(self.cell_center[0]**2 + self.cell_center[1]**2)

    # Ritorna il numero di oggetti nella cella
    def object_number(self):
        object_density = object_number_function(self.distance_to_center())
        object_number_int = int(object_density * self.area())
        return object_number_int
    
    # Ritorna una tupla contenente le coordinate di due oggetti interni alla cella
    def generate_coordinates(self):
        r.seed()
        x_object = rescale(r.randint(0, self.max_rand), self.max_rand, -self.side/2, self.side/2)
        y_object = rescale(r.randint(0, self.max_rand), self.max_rand, -self.side/2, self.side/2)
        return (x_object, y_object)

    # Costruisce la lista contenente tutti le tuple di coordinate interne alla cella
    def cell_coordinates(self):
        if self.local_coordinates != []:
            return self.local_coordinates

        total_number = self.object_number()
        for _ in range(total_number):
            coordinate_tuple = self.generate_coordinates()
            self.local_coordinates.append(coordinate_tuple)
        return self.local_coordinates

    # Converte le coordinate interne alla cella in coordinate globali
    def cluster_coordinates(self):
        if self.global_coordinates != []:
            return self.global_coordinates
        
        if self.local_coordinates == []:
            self.local_coordinates = self.cell_coordinates()
            
        for _ in self.local_coordinates:
            x_global = _[0] + self.cell_center[0]
            y_global = _[1] + self.cell_center[1]
            global_tuple = (x_global, y_global)
            self.global_coordinates.append(global_tuple)
        return self.global_coordinates

# Lavoro con gli arcosecondi e poi riconverto in arcominuti (sperando di non avere problemi con i decimali)


global_side = arcmin_to_arcsec(28) # 28 arcominuti, convertito poi in arcosecondi
subdivisions = 112 # Non oltre 112, altrimenti cominci a perdere oggetti
cell_side = global_side/subdivisions
print('Il lato della cella è pari a %f arcominuti' % arcsec_to_arcmin(cell_side))
cell_dict = {}
index = 0

start = t.time()
for i in range(subdivisions):
    for j in range(subdivisions):
        key = 'cell_' + str(i) + str(j)
        center_x = -global_side/2 + cell_side/2 + j*cell_side
        center_y = -global_side/2 + cell_side/2 + i*cell_side
        center = (arcsec_to_arcmin(center_x), arcsec_to_arcmin(center_y))
        cell_dict[key] = cell(arcsec_to_arcmin(cell_side), center, index)
        index += 1
stop = t.time()

print('Tempo necessario per la generazione delle celle: %f secondi' % (stop-start))
xy_coordinates = all_coordinates(cell_dict)

start = t.time()
close_coordinates = close_stars(xy_coordinates)
stop = t.time()
print('Numero totale di oggetti generati: %d \nTempo necessario per determinare oggetti vicini: %f secondi'
 % (len(xy_coordinates[0]), (stop-start)))

# Decommenta per vedere solo gli oggetti senza distinzioni
# ~ plt.gca().set_aspect('equal')
# ~ plot_something(xy_coordinates, 0.1, 'b')
# ~ plt.show()

# Decommenta per vedere tutti gli oggetti con evidenziati quelli non risolvibili
plt.gca().set_aspect('equal')  # Pareggia gli assi in modo che i cerchi appaiano tali

radius = 0
count = 0

for (i, j) in zip(close_coordinates[0], close_coordinates[1]):
    radius += np.sqrt(i**2 + j**2)
    count += 1

radius = radius/count
    
circle = plt.Circle((0,0), radius, color = 'k', fill = False)
plt.gcf().gca().add_artist(circle)

plot_something(xy_coordinates, 0.1, 'b')
plot_something(close_coordinates, 0.15, 'r')
plt.show()
