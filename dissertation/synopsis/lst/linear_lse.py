import numpy as np

def linear_lse(vals_x, vals_y):
    """Computes coefficients of the linear model using LSE method.

    Parameters:
        vals_x --- numpy array of free values
        vals_y --- numpy array of dependent values

    Return:
        computed parameters of the linear model
    """
    x_t = np.array((np.ones(vals_x.shape), vals_x))
    x = x_t.T
    est = np.dot(np.dot(np.linalg.inv(np.dot(x_t, x)), x_t), vals_y)
    return np.vstack(est)
