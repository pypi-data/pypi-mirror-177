"""Handles optimization for hyperparameters shared across
all kernels as part of the gridsearch_nmll function for
xGPRegression."""
try:
    import cupy as cp
except:
    pass
import numpy as np



def shared_hparam_search(z_trans_y, eigvals, nsamples,
                        y_trans_y, device, init_bounds, n_pts_per_dim,
                        n_cycles = 4, min_eigval = 1e-5):
    """Used by gridsearch_nmll under xGPRegression. Currently we use a 'telescoping
    grid' procedure to search the space, where we use several successive
    grids of finer resolution. We have experimented also with constrained
    optimization. The problem is that it is highly preferable to be able to
    guarantee the resulting hyperparameters yield a positive definite Z^T Z. This is
    easily enforced during grid search, harder to enforce during optimization.

    Args:
        z_trans_y: A cupy or numpy vector containing the product
            U^T @ Z^T @ y, where y is targets, Z is the random features
            and U is the eigenvectors of Z^T Z.
        eigvals: A cupy or numpy array containing the eigenvalues of
            Z^T Z.
        nsamples (int): The number of datapoints.
        y_trans_y (float): The product y^T y.
        device (str): One of "cpu", "gpu".
        init_bounds (np.ndarray): A 2 x 2 array where [0,:] is the boundaries
            for shared hyperparameter lambda and [1,:] is the boundaries
            for shared hyperparameter beta.
        n_pts_per_dim (int): The number of points per grid dimension.
        n_cycles (int): The number of 'telescoping grid' cycles.
        min_eigval (float): The smallest acceptable eigenvalue of Z^T Z + lambda I
            in order for the corresponding hyperparameter combination to be considered
            acceptable. Occasionally due to numerical error for very-close-to-singular
            matrices the marginal likelihood may be incorrectly calculated. The min_eigval
            threshold ensures that hyperparameter combinations which generate such matrices
            are ruled out and not considered as 'valid'. Setting a higher cutoff reduces
            the risk of this occurrence but increases the risk of occasionally ruling
            out an acceptable hyperparameter combination in error.

    Returns:
        score (float): The NMLL associated with the best lambda-beta values found.
        best_lb (np.ndarray): The best lambda and beta values found on optimization.
    """
    if device == "gpu":
        logfunc = cp.log
    else:
        logfunc = np.log
    bounds = init_bounds.copy()
    for i in range(n_cycles):
        lambda_, beta_, lambda_spacing, beta_spacing = get_grid_pts(bounds,
                            n_pts_per_dim, device)
        diag_term = lambda_[:,None]**2 + beta_[:,None]**2 * eigvals[None,:]

        min_eigvals = diag_term.min(axis=1)
        mask = min_eigvals > min_eigval
        diag_term = diag_term.clip(min = 1e-14)

        weights = beta_[:,None]**2 * (z_trans_y[None,:] / diag_term)
        scoregrid = y_trans_y - mask * (z_trans_y[None,:] * weights).sum(axis=1)
        scoregrid *= (0.5 / lambda_**2)
        scoregrid += (nsamples - eigvals.shape[0]) * logfunc(lambda_)
        scoregrid += 0.5 * (logfunc(diag_term) * mask[:,None]).sum(axis=1)
        scoregrid += nsamples * 0.5 * np.log(2 * np.pi)
        min_pt = scoregrid.argmin()
        best_score, best_lb = scoregrid[min_pt], [float(lambda_[min_pt]),
                                float(beta_[min_pt])]
        best_lb[0], best_lb[1] = np.log(best_lb[0]), np.log(best_lb[1])
        bounds[0,0] = max(best_lb[0] - lambda_spacing, init_bounds[0,0])
        bounds[0,1] = min(best_lb[0] + lambda_spacing, init_bounds[0,1])
        bounds[1,0] = max(best_lb[1] - beta_spacing, init_bounds[1,0])
        bounds[1,1] = min(best_lb[1] + beta_spacing, init_bounds[1,1])

    return float(best_score), np.asarray(best_lb)

def get_grid_pts(bounds, n_pts_per_dim, device):
    """Generates grid points for the two shared hyperparameters
    for a given set of boundaries.

    Args:
        bounds (np.ndarray): A 2 x 2 array where [0,:] is the boundaries
            for shared hyperparameter lambda and [1,:] is the boundaries
            for shared hyperparameter beta.
        device (str): One of "cpu", "gpu".
        n_pts_per_dim (int): The number of points per grid dimension.

    Returns:
        lambda_ (np.ndarray): The grid coordinates for the first hyperparameter.
        beta_ (np.ndarray): The grid coordinates for the second hyperparameter.
        lambda_spacing (float): The spacing between lambda grid points.
        beta_spacing (float): The spacing between beta grid points.
    """
    lambda_pts = np.linspace(bounds[0,0], bounds[0,1], n_pts_per_dim)
    beta_pts = np.linspace(bounds[1,0], bounds[1,1], n_pts_per_dim)
    lambda_pts, beta_pts = np.meshgrid(lambda_pts, beta_pts)
    lambda_ = np.exp(lambda_pts.flatten())
    beta_ = np.exp(beta_pts.flatten())
    lambda_spacing = 1.05 * np.abs(bounds[0,0] - bounds[0,1]) / n_pts_per_dim
    beta_spacing = 1.05 * np.abs(bounds[1,0] - bounds[1,1]) / n_pts_per_dim
    if device == "gpu":
        lambda_, beta_ = cp.asarray(lambda_), cp.asarray(beta_)
    return lambda_, beta_, lambda_spacing, beta_spacing
