import numpy as np
import sympy as sp

from stats.methods import search_lse

sym_expression = sp.sympify('a + b*sin(x)')
sym_alpha, sym_beta = sp.symbols('a b')
sym_x, sym_y = sp.symbols('x y')
measured_vals_x = np.array([...])
measured_vals_y = np.array([...])
lse_alpha, lse_beta = search_lse(
    expression=sym_expression,
    parameters=(sym_alpha, sym_beta),
    values={sym_x: measured_vals_x},
    result_values={sym_y: measured_vals_y},
    init_estimates={sym_alpha: 0, sym_beta: 0},
    num_iter=2)
