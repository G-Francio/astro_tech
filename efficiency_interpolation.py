import numpy as np
from scipy import interpolate as i
from scipy import integrate as integ
import matplotlib.pyplot as plt

x = []
y = []

with open('F555W.txt') as f:
    for line in f:
        new_line = line.split(' ')
        x.append(float(new_line[0]))
        y.append(float(new_line[1].rstrip()))

f.close()

f_interpolate = i.interp1d(x, y, kind = 'cubic')

max_pass = max(y)

tol = 0.5

check = 0
for (elem_x, elem_y) in zip(x, y):
    test = (elem_y/max_pass)*100
    if elem_x < x[y.index(max_pass)] and test <= tol and test > check:
        check = test
        start = elem_x

check = 0
for (elem_x, elem_y) in zip(x, y):
    test = (elem_y/max_pass)*100
    if elem_x > x[y.index(max_pass)] and test <= tol and test > check:
        check = test
        stop = elem_x

print('Start: %f, stop: %f, delta lambda: %f' % (start, stop, abs(start-stop)))

integral = integ.quad(f_interpolate, start, stop, points = x, limit = len(x))[0]
av_eff = integral/(stop-start)
print('Efficienza media: %f' % av_eff)

plt.plot(x, f_interpolate(x))
# plt.scatter(x, y, s = 2.5, c = 'g')
plt.scatter((start, stop), (f_interpolate(start), f_interpolate(stop)), c = 'r', s = 2.5)
plt.show()
    
