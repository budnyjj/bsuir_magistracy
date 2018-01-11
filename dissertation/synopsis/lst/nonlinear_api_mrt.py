import numpy as np
import sympy as sp

from stats.methods import search_mrt

sym_expression_delta = sp.sympify('y - (a + b*sin(x))')
sym_alpha, sym_beta = sp.symbols('a b')
sym_x, sym_y = sp.symbols('x y')
measured_vals_x = np.array([...])
measured_vals_y = np.array([...])
mrt_params = search_mrt(
    delta_expression=sym_expression_delta,
    parameters=(sym_alpha, sym_beta),
    values={sym_x: measured_vals_x, sym_y: measured_vals_y},
    err_stds={sym_x: 1, sym_y: 1})
