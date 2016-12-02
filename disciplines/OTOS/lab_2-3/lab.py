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

def meter(val, transform, disp):
    return transform*val + random.gauss(0, math.sqrt(disp))

def filter_kalman(vals, model_fi, model_avg, model_disp, meter_transform, meter_disp):
    result = []
    est_filtered = model_avg
    disp_filtered = model_disp
    for val in vals:
        est_extrapolated = model_fi * est_filtered
        disp_extrapolated = model_disp + model_fi*disp_filtered*model_fi
        gain = (disp_extrapolated*meter_transform) / (meter_transform*disp_extrapolated*meter_transform + meter_disp)
        print("gain:", gain)
        est_filtered = est_extrapolated + gain*(val - meter_transform*est_extrapolated)
        disp_filtered = disp_extrapolated - gain*meter_transform*disp_filtered
        result.append(gain)
    return result

NUM_ITER = 10
# model parameters
MODEL_AVG = 0
MODEL_SIGMA2 = 8
MODEL_ALPHA = 0.008
MODEL_PERIOD = 40
# meter parameters
METER_TRANSFORM = 1
METER_DISP = 0.1

MODEL_FI = math.exp(-MODEL_ALPHA*MODEL_PERIOD)
MODEL_DISP = MODEL_SIGMA2*(1-math.exp(-2*MODEL_ALPHA*MODEL_PERIOD))

vals_t = []
vals_x = []
vals_m = []
for i,val_x in enumerate(model(MODEL_FI, MODEL_AVG, MODEL_DISP, NUM_ITER)):
    vals_t.append(i*MODEL_PERIOD)
    vals_x.append(val_x)
    vals_m.append(meter(val_x, METER_TRANSFORM, METER_DISP))

vals_fm = filter_kalman(vals_m,
                        MODEL_FI, MODEL_AVG, MODEL_DISP,
                        METER_TRANSFORM, METER_DISP)

plt.plot(vals_t, vals_x,
         color='r', linestyle=' ',
         marker='.', markersize=5)
plt.plot(vals_t, vals_m,
         color='g', linestyle='-')
plt.plot(vals_t, vals_fm,
         color='b', linestyle='-')


plt.grid(True)
plt.xlabel('$ t $')
plt.ylabel('$ x $')
plt.savefig('plot.png', dpi=200)
