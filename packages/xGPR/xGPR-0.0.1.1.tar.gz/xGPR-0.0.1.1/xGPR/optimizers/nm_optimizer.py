"""Describes the lbfgs_optimizer function for performing L-BFGS
based hyperparameter optimization."""
import numpy as np
from scipy.optimize import minimize

def nelder_mead_optimizer(dataset, cost_fun, bounds,
                    max_iter, init_hyperparams,
                    verbose=True, tol=1e-2):
    """Performs a single restart of nelder-mead optimization from
    a designated starting point.

    Args:
        dataset: An OnlineDataset or OfflineDataset containing the
            raw data.
        cost_fun: A function that calculates and returns the
            negative marginal log-likelihood (a float) for given
            hyperparameters and an OnlineDataset or OfflineDataset
            object.
        max_iter (int): The maximum number of iterations per restart.
        init_hyperparams (np.ndarray): A length N
            numpy array containing the starting point for optimization.
        verbose (bool): If True, regular updates are printed during
            optimization.
        tol (float): Tolerance for convergence.

    Returns:
        hyperparams (np.ndarray): The best hyperparameters identified.
        score (float): The best score achieved.
        niter (int): The number of iterations.
    """
    bounds_tuples = list(map(tuple, bounds))
    if verbose:
        print("Now beginning NM minimization.")
    try:
        res = minimize(cost_fun, x0 = init_hyperparams,
                options={"maxiter":max_iter, "xatol":tol},
                    method="Nelder-Mead",
                    args = (dataset,verbose,True),
                    bounds = bounds_tuples)
    except Exception as e:
        print(e)
        if verbose:
            print("Error encountered "
                        "during NM minimization.")
        return init_hyperparams, np.inf, 0
    if verbose:
        print(f"NM optimization complete, score is {res.fun}")
    return res.x, res.fun, res.nfev
