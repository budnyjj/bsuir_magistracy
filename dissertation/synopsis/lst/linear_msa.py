import numpy as np

def linear_sa(vals_x, vals_y):
    """
    Computes coefficients of the linear model using SA method.

    Parameters:
        vals_x --- numpy array of free values
        vals_y --- numpy array of dependent values

    Return:
        computed parameters of the linear model
    """
    num_rows_x = 1 if len(vals_x.shape) == 1 \
                 else vals_x.shape[0]
    vals = np.vstack((vals_x, vals_y))
    avg_vals = np.mean(vals, axis=1)
    cov_vals = np.cov(vals)
    eig_vals, eig_vectors = np.linalg.eig(cov_vals)
    # sort eigenvectors using the order of corresponding
    # eigenvectors: from biggest to smallest and take the
    # num_rows_x largest ones
    eig_vals_order = np.argsort(-eig_vals)
    eig_vectors_t = eig_vectors.transpose()
    c = eig_vectors_t[eig_vals_order][:num_rows_x].transpose()
    est_x0 = avg_vals[:num_rows_x]
    est_alpha = avg_vals[num_rows_x:]
    c_top = c[:num_rows_x]
    c_bottom = c[num_rows_x:]
    est_beta = np.dot(c_bottom, np.linalg.inv(c_top))
    return (est_alpha - np.dot(est_beta, est_x0),
            est_beta.flatten())
