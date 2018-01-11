import sympy as sp
import numpy as np

# Caches results of symbolical equation solving
__CACHE_SOLUTIONS = {}
# Caches result of symbolic parameter substitutions
__CACHE_SUBSTITUTIONS = {}

# Helper functions
def __gen_subs(f_subs, values):
    """
    Generates dicts of substitutions of f_subs symbolic
    variables by corresponding values with equal
    distance between them.

    Parameters:
        f_subs --- tuple of dicts with indexed symbolical
            values, keyed by these symbolical values,
            for example: [{x: x1, y: y1}, {x: x2, y: y2}]
        values --- dict of values, keyed by sympy objects,
            for example, {x: [x1, x2, ...], y: [y1, y2, ...])

    Yield:
        dict of substitutions, for example:
            {x1: 12, x2: 21, y1: 43, y2: 34}
    """
    # get sample parameter as first key of dict
    s_p = next(iter(values.keys()))
    # determine distance between neighbour values,
    # for example x0 and x1
    distance = len(values[s_p]) // len(f_subs)
    # result substitution
    res = {}
    for val_i in range(distance):
        for f_subs_i, f_sub in enumerate(f_subs):
            for sym_value in values:
                # param to substitute
                f_subs_param = f_sub[sym_value]
                # index of current value
                cur_val_i = val_i + f_subs_i * distance
                res[f_subs_param] = \
                    values[sym_value][cur_val_i]
        yield res
def __gen_equations(delta_expression, values, num_params):
    """
    Provides system of equations from delta_expression for
    every parameter and list of symbolic substitutions for
    each equation.

    Parameters:
        delta_expression --- sympy object, which represents
            equation, for example: 'a * exp(-alpha*x) - y',
            which has to be equal to 0
        values --- dict of values, keyed by sympy objects,
            for example: {x: [x1, x2, ...], y: [y1, y2, ...])
        num_params --- number of target parameters in
            delta_expression

    Return:
        list of equations, generated from delta expression
        list of dicts with of indexed symbolical_values,
            keyed by these symbolical values,
            for example: [{x: x1, y: y1}, {x: x2, y: y2}]
    """
    # vector function
    f = []
    # vector function substitutions
    f_subs = []
    # generate system of equations
    for param_i in range(num_params):
        # generate substitutions: x -> x1, y -> y1, ...
        # for each equation
        subs = {}
        for sym_value in values:
            subs[sym_value] = \
                sp.Symbol('{}{}'.format(sym_value, param_i))
        f.append(delta_expression.subs(subs))
        f_subs.append(subs)
    return tuple(f), tuple(f_subs)












def __subs(sym_f, subs):
    """
    Computes values of function by value substitution.

    Parameters:
        sym_f --- symbolic function to evaluate,
            for example: (y0 - y1)/(x0 - x1)
        subs --- dict of symbolic/numeric substitutions,
            for example: {x0: 8.98, y0: 8.98,
                          x1: 9.31, y1: 9.31}

    Return:
        computed value as the result of numeric
        parameter substitutions
    """
    sym_subs, val_subs = tuple(subs.keys()), subs.values()
    key_sub = (sym_f, sym_subs)
    f = None
    try:
        f = __CACHE_SUBSTITUTIONS[key_sub]
    except KeyError:
        f = sp.lambdify(sym_subs, sym_f, modules='numpy')
        __CACHE_SUBSTITUTIONS[key_sub] = f
    val_f = f(*val_subs)
    return val_f

def __solve(f, parameters):
    """
    Provides result of symbolic equation solving.

    Parameters:
        f --- tuple of sympy equations to solve
        parameters --- tuple of sympy parameters of equation

    Return:
        first sympy solution of equation
    """
    key_solution = (f, parameters)
    solution = None
    try:
        solution = __CACHE_SOLUTIONS[key_solution]
    except KeyError:
        solution = sp.solve(f, parameters, dict=True)
        __CACHE_SOLUTIONS[key_solution] = solution
    if type(solution) is list:
        # get only first solution
        solution = solution[0]
    return solution
# Method
def search_mrt(delta_expression, parameters, values, err_stds):
    """
    Computes estimates using Taylor method.

    Parameters:
        delta_expression --- sympy object, which represents
            equation, for example, 'a * exp(-alpha*x) - y',
            which should be equal to 0
        parameters --- tuple of sympy objects, whose estimates
            should be found, for example, (a, alpha)
        values --- dict of values, keyed by sympy objects,
            for example, {x: [x1, x2, ...], y: [y1, y2, ...])
        err_stds --- dict of standart error deviations of
            values, keyed by sympy objects,
            for example: {x: 0.2, y: 0.2}

    Return:
         computed estimates of symbolic parameters
    """
    # number of symbolic parameters
    num_params = int(len(parameters))
    # get list of symbolic values
    sym_vals = tuple(values.keys())
    # number of symbolic values
    num_sym_vals = int(len(sym_vals))
    # generate parameter equations
    f, f_subs = __gen_equations(
        delta_expression, values, num_params)
    # symbolic expressions of parameters
    sym_expr_params = __solve(f, parameters)
    # matrix of symbolic derivatives
    sym_G = []
    # compute derivarives of parameter expressions,
    # and place into matrix, for example:
    # G = [
    #       [ diff(expr1, x0), diff(expr1, y0),
    #         diff(expr1, x1), diff(expr1, y1) ],
    #       [ diff(expr2, x0), diff(expr2, y0),
    #         diff(expr2, x1), diff(expr2, y1) ],
    #     ], where x0, x1, y0, y1 are sym_values
    for parameter in parameters:
        g_row = []
        for f_sub in f_subs:
            for sym_val in sym_vals:
                g_row.append(
                    sp.diff(sym_expr_params[parameter],
                            f_sub[sym_val]))
        sym_G.append(g_row)
    # create diagonal matrix of error dispersions
    err_disps = np.zeros(num_params * num_sym_vals)
    err_disp_i = 0
    for _ in parameters:
        for sym_val in sym_vals:
            err_disps[err_disp_i] = err_stds[sym_val] ** 2
            err_disp_i += 1
    R_err = np.diagflat(err_disps)
    # accumulation matrix with summary of R
    sum_R_inv = np.zeros((num_params, num_params))
    # accumulation matrix with summary of R_inv * theta
    sum_R_inv_theta = np.zeros(num_params)
    # replace symbolic values of f_subs with real values
    for val_subs in __gen_subs(f_subs, values):
        G = np.zeros((len(sym_G), len(sym_G[0])))
        for i, sym_g_row in enumerate(sym_G):
            for j, sym_diff in enumerate(sym_g_row):
                G[i, j] = __subs(sym_diff, val_subs)
        R = np.dot(np.dot(G, R_err), G.T)
        R_inv = np.linalg.inv(R)
        sum_R_inv += R_inv
        # substitute values into sym_expr_param to get theta
        theta = np.zeros((num_params, 1))
        for (i_param, param) in enumerate(parameters):
            theta[i_param, 0] = \
                __subs(sym_expr_params[param], val_subs)
        R_inv_theta = np.dot(R_inv, theta)
        sum_R_inv_theta = sum_R_inv_theta + R_inv_theta
    res_matrix = np.dot(np.linalg.inv(sum_R_inv),
                        sum_R_inv_theta)
    estimates = res_matrix[:,0]
    return estimates
