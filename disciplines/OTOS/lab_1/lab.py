#!/usr/bin/env python

import functools
import math
import random

import numpy as np
import matplotlib.pyplot as plt

plt.rc('text', usetex=True)
plt.rc('font', family='serif')


# 1D model
def model(x):
    a = 2.7; d = 0.1; y_0 = 2
    sigma = 0.001
    result = y_0 - 0.04 * (x - a) - d * (x - a)**2
    return result + random.gauss(0, sigma)

def search_asymmetric(model, start_x, num_iter=100):
    next_x = cur_x = start_x
    vals_x = [cur_x]
    for k in range(num_iter):
        alpha = (k + 1) ** (-1/3)
        factor = (k + 1) ** (-2/3)
        next_x = cur_x + factor * (model(cur_x + alpha) - model(cur_x))
        cur_x = next_x
        vals_x.append(cur_x)
    return vals_x

def search_symmetric(model, start_x, num_iter=100):
    next_x = cur_x = start_x
    vals_x = [cur_x]
    for k in range(num_iter):
        alpha = (k + 1) ** (-1/3)
        factor = (k + 1) ** (-2/3)
        next_x = cur_x + factor * (model(cur_x + alpha) - model(cur_x - alpha))
        cur_x = next_x
        vals_x.append(cur_x)
    return vals_x


NUM_ITER = 1000
MIN_X = 1; MAX_X = 10; NUM_X = 100
VALS_X = np.linspace(MIN_X, MAX_X, NUM_X)

model_vec = np.vectorize(model)

plt.plot(VALS_X, model_vec(VALS_X),
         color='r', linestyle=' ',
         marker='.', markersize=5,
         label='model')

search_asymmetric_x = search_asymmetric(model, MAX_X, NUM_ITER)
plt.plot(search_asymmetric_x, model_vec(search_asymmetric_x),
         color='g', marker='x', markersize=5,
         label='asymmetric')

search_symmetric_x = search_symmetric(model, MAX_X, NUM_ITER)
plt.plot(search_symmetric_x, model_vec(search_symmetric_x),
         color='b',  marker='x', markersize=5,
         label='symmetric')


plt.xlabel('$ x $')
plt.ylabel('$ y $')
plt.grid(True)
# plt.legend(loc=2)
plt.savefig('plot.png', dpi=200)
