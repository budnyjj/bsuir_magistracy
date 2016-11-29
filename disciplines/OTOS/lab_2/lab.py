#!/usr/bin/env python

import functools
import math
import random

import numpy as np
import matplotlib.pyplot as plt

plt.rc('text', usetex=True)
plt.rc('font', family='serif')


def model(avg, disp, period, num_iter):
    alpha = 0.008
    sigma = math.sqrt(disp*(1-math.exp(-2*alpha*period)))
    cur_val = avg + random.gauss(0, sigma)
    for _ in range(num_iter):
        new_val = avg + math.exp(-alpha*period)*(cur_val - avg) + random.gauss(0, sigma)
        cur_val = new_val
        yield new_val


AVG = 0
DISP = 8
PERIOD = 130
NUM_ITER = 100

vals_x = []
vals_y = []
for i,val_y in enumerate(model(AVG, DISP, PERIOD, NUM_ITER)):
    vals_x.append(i*PERIOD)
    vals_y.append(val_y)

plt.plot(vals_x, vals_y,
         color='r', linestyle=' ',
         marker='.', markersize=5)
plt.grid(True)
plt.xlabel('$ t $')
plt.ylabel('$ x $')
plt.savefig('plot.png', dpi=200)
