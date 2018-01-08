import sympy as sp
import numpy as np

def search_lse(expression, parameters, values, result_values, init_estimates, num_iter=1):
    """
    Computes estimates of ditribution parameters with LSE method.

    Parameters:
        expression --- sympy object, which represents target expression,
            for example, 'a * exp(-alpha*x)'
        parameters --- list of sympy objects, whose estimates we should find,
            for example, (a, alpha)
        values --- dict of values, keyed by sympy objects,
            for example, {x: [x1, x2, ...]}
        result_values --- dict of result values, keyed by sympy objects
            for example, {y: [y1, y2, ...]}
        init_estimates --- dict of init values of estimates,
            used in iterational search of estimates, keyed by sympy objects,
            for example: {x: 0, y: 0}
        err_stds --- dict of standart error deviations of values, keyed by sympy objects,
            for example: {x: 0.2, y: 0.2}
        num_iter --- number of method iterations
    Yield:
         number of iteration, computed estimates of symbolic parameters
    """
    # get list of symbolic values
    sym_vals = tuple(values.keys())
    # get array of real values
    vals = []
    for sym_val in sym_vals:
        vals.append(values[sym_val])
    vals = np.array(vals).T
    # get result values as first value of dict
    res_vals = [next(iter(result_values.values()))]
    res_vals = np.array(res_vals).T
    # init effective estimates with basic values
    cur_estimates = []
    for parameter in parameters:
        cur_estimates.append(init_estimates[parameter])
    cur_estimates = np.array([cur_estimates]).T
    # get matrix of symbolic derivatives of expression
    sym_diff_funcs = []
    for parameter in parameters:
        sym_diff_funcs.append(sp.diff(expression, parameter))
    for i in range(num_iter):
        # substitute current parameter values into sym_expr
        subs = {}
        for i_param, sym_param in enumerate(parameters):
            subs[sym_param] = cur_estimates[i_param]
        cur_f = sp.lambdify(sym_vals, expression.subs(subs), 'numpy')
        cur_appr = np.vectorize(cur_f)(vals)
        # compute derivates of sym_expr by sym_params
        diff_funcs = []
        for param_i, parameter in enumerate(parameters):
            diff_func = sym_diff_funcs[param_i].subs(subs)
            diff_funcs.append(sp.lambdify(sym_vals, diff_func, 'numpy'))
        # construct Q from rows
        q_rows = []
        for diff_func in diff_funcs:
            q_rows.append(
                np.vectorize(diff_func)(vals)
            )
        Q = np.hstack(q_rows)
        Q_t = Q.T
        # calculate addition = ((Q_t*Q)^-1)*Q_t*(res_vals - cur_appr)
        add = np.dot(np.dot(np.linalg.inv(np.dot(Q_t, Q)), Q_t), res_vals - cur_appr)
        cur_estimates += add
        # yield first row
        yield i + 1, cur_estimates.T[0]
