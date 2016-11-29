#!/usr/bin/env python

import functools
import math
import random

import numpy as np
import matplotlib.pyplot as plt

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D

# generates orthogonal vectors of specified size
def gen_orts(num_dims):
    for i in range(num_dims):
        e = np.zeros(num_dims)
        e[i] = 1
        yield e

# plots 3D representation of function
def plot2(f, val_x, val_y, filename):
    mesh_val_x, mesh_val_y = np.meshgrid(val_x, val_y)
    mesh_r = np.vectorize(f)(mesh_val_x, mesh_val_y)

    figure = plt.figure()
    ax = figure.gca(projection='3d')
    surface = ax.plot_surface(mesh_val_x, mesh_val_y, mesh_r,
                              rstride=1, cstride=1, cmap=cm.coolwarm,
                              linewidth=0)

    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    plt.savefig(filename, dpi=200)
    figure.clear()

# 1D model
def f_1(val_x, sigma):
    a = 2.7; d = 0.1; y_0 = 2
    result = y_0 - 0.04 * ((val_x - a) - d * (val_x - a)**2)
    return result + random.gauss(0, sigma)

# 2D model
def f_2(val_x1, val_x2, sigma):
    y_0 = 2

    a = 2.7
    A = np.array([a, a])

    r = 0.3
    d_11 = 0.2; d_22 = 0.3; d_12 = r * math.sqrt(d_11 * d_22)
    D = np.array([[d_11, d_12], [d_12, d_22]])

    vec_x = np.array([val_x1, val_x2])
    vec_diff = vec_x - A
    result = y_0 - np.dot(np.dot(vec_diff, D), vec_diff.T)
    return result + random.gauss(0, sigma)

def search_asymmetric(model, start_vals, eps=0.0001):
    num_dims = len(start_vals)
    k = 0
    next_vals = cur_vals = start_vals
    for _ in range(5):
        k += 1
        alpha = k ** (-1/3)
        factor = k ** (-2/3)
        print("cur_vals: ", cur_vals)
        diff = np.zeros(num_dims)
        for ort in gen_orts(num_dims):
            print("ort: ", ort)
            ort_step = alpha * ort
            print("ort_step: ", ort_step)
            ort_vals = cur_vals + ort_step
            print("ort_vals: ", ort_vals)
            ort_diff = (model(*ort_vals) - model(cur_vals)) * ort
            print("ort_diff: ", ort_diff)
            diff += ort_diff
            print()
        next_vals = cur_vals + diff * factor
        print("next_vals: ", next_vals)
        print()
        cur_vals = next_vals

def search_symmetric(model, start_vals, eps=0.0001):
    num_dims = len(start_vals)
    k = 0
    next_vals = cur_vals = start_vals
    for _ in range(10000):
        k += 1
        alpha = k ** (-1/3)
        factor = k ** (-2/3)
        print("cur_vals: ", cur_vals)
        diff = np.zeros(num_dims)
        for ort in gen_orts(num_dims):
            print("ort: ", ort)
            ort_step = alpha * ort
            print("ort_step: ", ort_step)
            ort_vals_minus = cur_vals - ort_step
            print("ort_vals_minus: ", ort_vals_minus)
            ort_vals_plus = cur_vals + ort_step
            print("ort_vals_plus: ", ort_vals_plus)
            ort_diff = (model(*ort_vals_plus) - model(*ort_vals_minus)) * ort
            print("ort_diff: ", ort_diff)
            diff += ort_diff
            print()
        next_vals = cur_vals + diff * factor
        print("next_vals: ", next_vals)
        print()
        cur_vals = next_vals


    # num_dims = len(start_vals)
    # cur_err = eps
    # k = 0
    # next_vals = cur_vals = start_vals
    # while cur_err >= eps:
    #     k += 1; alpha = k ** (-1/3); factor = k ** (-2/3)
    #     print("cur_vals: ", cur_vals)
    #     cur_results = model(*cur_vals)
    #     print("cur_results: ", cur_results)
    #     ort_vals = np.zeros(num_dims)
    #     for ort in gen_orts(num_dims):
    #         print("alpha * ort: ", alpha * ort)
    #         step_ort_vals = cur_vals + alpha * ort
    #         print("step_ort_vals: ", step_ort_vals)
    #         diff_ort_vals = model(*step_ort_vals) - cur_results
    #         print("diff_ort_vals: ", diff_ort_vals)
    #         ort_vals += diff_ort_vals * ort
    #         print("ort_vals: ", ort_vals)
    #     next_vals = cur_vals + factor * ort_vals
    #     print("next_vals: ", next_vals)
    #     cur_diff = abs(next_vals - cur_vals)
    #     cur_err = np.dot(cur_diff, cur_diff.T)
    #     cur_vals = next_vals
    #     print()
    # return cur_vals

SIGMA = 0.0001
MIN_X = 0; MAX_X = 10; NUM_X = 10
MIN_Y = 0; MAX_Y = 10; NUM_Y = 10

MODEL_1 = functools.partial(f_1, sigma=SIGMA)
MODEL_2 = functools.partial(f_2, sigma=SIGMA)

VALS_X = np.linspace(MIN_X, MAX_X, NUM_X)
VALS_Y = np.linspace(MIN_Y, MAX_Y, NUM_Y)

plt.plot(VALS_X, np.vectorize(MODEL_1)(VALS_X))
plt.savefig('plot.png', dpi=200)

print(search_symmetric(MODEL_1, np.array([MIN_X])))

# plot2(MODEL_2, VALS_X, VALS_Y, 'plot2.png')
# print(search_asymmetric(MODEL_2, np.array([MIN_X, MIN_Y])))

    # One-dimension
    # Y = []
    # for x in X:
    #     y = model([x], sigma)
    #     Y.append(y)
    #     # print(x, y)

    # plt.plot(X, Y)
    # plt.show()
