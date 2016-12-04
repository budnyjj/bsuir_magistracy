#!/usr/bin/env python

import functools
import math
import random

import numpy as np
import matplotlib.pyplot as plt

plt.rc('text', usetex=True)
plt.rc('font', family='serif')


def model(fi, avg, disp, num_iter):
    sigma = math.sqrt(disp)
    cur_val = avg + random.gauss(0, sigma)
    for _ in range(num_iter):
        new_val = avg + fi*(cur_val - avg) + random.gauss(0, sigma)
        cur_val = new_val
        yield new_val

def meter(val, hi, disp):
    return hi*val + random.gauss(0, math.sqrt(disp))

class FilterKalman:
    def __init__(self, model_fi, model_avg, model_disp, meter_hi, meter_disp):
        self.model_fi = model_fi
        self.model_avg = model_avg
        self.model_disp = model_disp
        self.meter_hi = meter_hi
        self.meter_disp = meter_disp
        self.est_filtered = model_avg
        self.disp_filtered = model_disp
        self.iteration = 0

    def filter(self, val):
        self.iteration += 1
        if (self.iteration == 1):
            return self.est_filtered
        est_extrapolated = self.model_fi * self.est_filtered
        disp_extrapolated = self.model_disp + (self.model_fi**2)*self.disp_filtered
        gain = disp_extrapolated * self.meter_hi
        gain /= (self.meter_hi**2)*disp_extrapolated + self.meter_disp
        self.est_filtered = est_extrapolated + gain*(val - self.meter_hi*est_extrapolated)
        self.disp_filtered = disp_extrapolated - gain*self.meter_hi*disp_extrapolated
        return self.est_filtered

NUM_ITER = 100
# model parameters
MODEL_AVG = 0
MODEL_SIGMA2 = 0.1
MODEL_ALPHA = 0.008
MODEL_PERIOD = 40
# meter parameters
METER_HI = 1
METER_DISP = 1

MODEL_FI = math.exp(-MODEL_ALPHA*MODEL_PERIOD)
# MODEL_FI = 1.05
MODEL_DISP = MODEL_SIGMA2*(1-math.exp(-2*MODEL_ALPHA*MODEL_PERIOD))

vals_t = []
vals_model = []
vals_meter = []
vals_filter = []
kalman = FilterKalman(MODEL_FI, MODEL_AVG, MODEL_DISP, METER_HI, METER_DISP)
for i,val_model in enumerate(model(MODEL_FI, MODEL_AVG, MODEL_DISP, NUM_ITER)):
    vals_t.append(i)
    vals_model.append(val_model)
    val_meter = meter(val_model, METER_HI, METER_DISP)
    vals_meter.append(val_meter)
    vals_filter.append(kalman.filter(val_meter))

plt.plot(vals_t[10:], vals_model[10:],
         color='r', linestyle='-',
         marker='.', markersize=5,
         label='real')
plt.plot(vals_t[10:], vals_meter[10:],
         color='g', linestyle='-',
         label='metered')
plt.plot(vals_t[10:], vals_filter[10:],
         color='b', linestyle='-',
         label='filtered')

plt.grid(True)
plt.xlabel('$ T $')
plt.ylabel('$ x $')
plt.legend(loc=2)


plt.savefig('plot.png', dpi=200)
