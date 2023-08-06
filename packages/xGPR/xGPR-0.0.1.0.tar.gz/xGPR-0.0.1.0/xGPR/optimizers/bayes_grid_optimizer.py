"""Describes the bayes_grid optimization routine, which uses a combination
of accelerated gridsearch (to reduce 4d and 3d problems to 2d and 1d)
with Bayesian optimization to find good hyperparameters."""
import warnings

import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor as GPR
from sklearn.gaussian_process.kernels import Matern

from ..constants import constants

def bayes_grid_tuning(cost_fun, dataset, bounds,
                    random_state, max_iter, verbose, tol = 1e-2,
                    min_eigval = 1e-5, init_pts = 0,
                    grid_pts_per_lb = 40):
    """Conducts accelerated gridsearch optimization + Bayesian
    optimization.

    Args:
        cost_fun: A function that takes as input a set of specified
            sigma_pts (kernel-specific hyperparameters), an lb_grid
            (a grid of lambda - beta or shared hyperparameter values),
            a dataset and optimization bounds, and returns
            a best negative marginal loglik achieved plus the hyperparams
            that achieved it.
        dataset: An OnlineDataset or OfflineDataset containing raw data.
        bounds (np.ndarray): An N x 2 for N hyperparameters set of boundaries
            for optimization.
        random_state (int): A seed for the random number generator.
        max_iter (int): The maximum number of iterations.
        verbose (bool): If True, print regular updates.
        tol (float): The threshold for convergence.
        min_eigval (float): The smallest acceptable eigenvalue of Z^T Z + lambda I
            in order for the corresponding hyperparameter combination to be considered
            acceptable. Occasionally due to numerical error for very-close-to-singular
            matrices the marginal likelihood may be incorrectly calculated. The min_eigval
            threshold ensures that hyperparameter combinations which generate such matrices
            are ruled out and not considered as 'valid'. Setting a higher cutoff reduces
            the risk of this occurrence but increases the risk of occasionally ruling
            out an acceptable hyperparameter combination in error. This does not usually
            need to be adjusted unless using single precision tuning.
        init_pts (int): If 0, the optimizer uses a reasonable number
            of starting points depending on dimensionality. Otherwise, init_pts is used.
        grid_pts_per_lb (int): The number of points to use on the grid for evaluating
            lambda/beta. Since the grid is evaluated 4x at increasing scales of resolution,
            the default of 40 is usually sufficient, but can be overriden if desired.

    Raises:
        ValueError: A ValueError is raised if this is run with a kernel with >
            5 or <= 2 hyperparameters.
    """

    if bounds.shape[0] > 5 or bounds.shape[0] < 3:
        raise ValueError("Bayesian optimization is only allowed for kernels with "
                "3 - 5 hyperparameters.")

    if init_pts <= 0:
        start_pt_defaults = [constants.NUM_INIT_BAYES_GRID_3D, 15, 25]
        num_start_pts = start_pt_defaults[[3,4,5].index(bounds.shape[0])]
    else:
        num_start_pts = init_pts
    if bounds.shape[0] == 3:
        sigma_grid,_ = get_grid_pts(num_start_pts, bounds)
    else:
        sigma_grid = get_random_starting_pts(15, bounds, random_state)

    lb_vals, scores = [], []
    if len(sigma_grid.shape) == 1:
        sigma_grid = sigma_grid.reshape(-1,1)
    sigma_grid = list(sigma_grid)
    for i, sigma_pt in enumerate(sigma_grid):
        score, lb_val = cost_fun(sigma_pt, dataset, bounds[:2,:], grid_pts_per_lb,
                                   min_eigval)

        scores.append(score)
        lb_vals.append(lb_val)
        if verbose:
            print(f"Grid point {i} acquired.")

    scores = np.asarray(scores)
    #The gridsearch function assigns 'np.inf' to points where
    #the resulting matrix would be extremely ill-conditioned.
    #We reset these to the smallest non-inf value.
    smallest_non_inf_val = np.max(scores[scores < np.inf])
    scores[scores == np.inf] = smallest_non_inf_val
    scores = scores.tolist()
    surrogate = GPR(kernel = Matern(nu=5/2),
            normalize_y = True,
            alpha = 1e-6, random_state = random_state,
            n_restarts_optimizer = 4)

    sigma_bounds = bounds[2:, :]
    for iternum in range(len(sigma_grid), max_iter):
        new_sigma, min_dist, surrogate = propose_new_point(
                            sigma_grid, scores, surrogate,
                            sigma_bounds, random_state + iternum)
        if verbose:
            print("New hparams: %s"%new_sigma)
        score, lb_val = cost_fun(new_sigma, dataset, bounds[:2,:], grid_pts_per_lb,
                                 min_eigval)
        sigma_grid.append(new_sigma)
        lb_vals.append(lb_val)
        scores.append(min(score, smallest_non_inf_val))

        if iternum > 15 and min_dist < tol:
            break
        if verbose:
            print(f"Additional acquisition {iternum}.")

    best_hparams = np.empty((bounds.shape[0]))
    best_hparams[2:] = sigma_grid[np.argmin(scores)]
    best_hparams[:2]  = lb_vals[np.argmin(scores)]
    if verbose:
        print(f"Best score achieved: {np.min(scores)}")
        print(f"Best hyperparams: {best_hparams}")
    return best_hparams, (sigma_grid, scores), np.min(scores), iternum


def propose_new_point(sigma_vals, scores,
                surrogate, bounds, random_state,
                num_cand = 500):
    """Refits the 'surrogate' model and uses it to propose new
    locations for exploration (via Thompson sampling).

    Args:
        sigma_vals (np.ndarray): A grid of kernel-specific hyperparameters
            at which NMLL has been evaluated so far.
        scores (array-like): The scores for sigma_vals.
        surrogate: A scikit-learn Gaussian process model with a Matern kernel.
            Is fitted to sigma_vals, scores.
        bounds (np.ndarray): An N x 2 for N kernel specific hyperparameters
            array of boundaries for optimization.
        random_state (int): A seed for the random number generator.
        num_cand (int): The number of candidate points to evaluate.

    Returns:
        best_candidate (np.ndarray): A set of kernel-specific hyperparameters
            at which to propose the next acquisition.
        min_dist (float): The smallest distance between best_candidate
            and any existing candidates.
        surrogate: The Gaussian process acquisition model now refitted
            to the updated data.
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        xvals = np.vstack(sigma_vals)
        surrogate.fit(xvals, scores)

    rng = np.random.default_rng(random_state)
    candidates = rng.uniform(low=bounds[:,0], high=bounds[:,1],
                           size = (num_cand, bounds.shape[0]))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        y_candidates = surrogate.sample_y(candidates, n_samples=15,
                    random_state=random_state)
    best_idx = np.unravel_index(y_candidates.argmin(),
                            y_candidates.shape)
    best_cand = candidates[best_idx[0],:]
    min_dist = np.min(np.linalg.norm(best_cand[None,:] - xvals, axis=1))
    return candidates[best_idx[0],:], min_dist, surrogate


def get_random_starting_pts(num_sigma_vals, bounds, random_seed = 123):
    """For kernels with 4 or 5 hyperparameters, it is often more efficient
    to randomly populate the search space with an initial number of search
    points, and then build on these with Bayesian optimization. This function
    generates the lambda_beta grid plus random 'exploration' values for
    the kernel-specific hyperparameters (aka 'sigma').

    Args:
        num_sigma_vals (int): The number of kernel-specific hyperparameter
            combinations to sample.
        bounds (np.ndarray): The boundaries of the search space.
        random_seed (int): A seed to the random number generator.

    Returns:
        sigma_grid (np.ndarray): The initial kernel-specific hyperparameter combinations to
            evaluate.
        lambda_beta_grid (np.ndarray): The shared hyperparameter combinations to evaluate for each
            sigma combination.
    """
    rng = np.random.default_rng(random_seed)
    sigma_grid = np.empty((num_sigma_vals, bounds.shape[0] - 2))
    for i in range(sigma_grid.shape[1]):
        sigma_grid[:,i] = rng.uniform(size = num_sigma_vals,
                        low = bounds[i + 2, 0], high = bounds[i + 2, 1])
    return sigma_grid


def get_grid_pts(num_pts_per_sigma, bounds):
    """Builds a starting grid of sigma points (kernel-specific
    hyperparameters).
    Args:
        num_pts_per_sigma (int): The number of points at which to
            evaluate NMLL per kernel-specific hyperparameter.
        bounds (np.ndarray): A numpy array of shape N x 2 for N
            hyperparameters indicating the boundaries within which
            to optimize.
    Returns:
        sigma_pts: Either [None] or a numpy array of shape
            (num_pts_per_axis, C) where C is the number of kernel-
            specific hyperparameters. NMLL is evaluated at each
            row in sigma_pts.
    """
    if bounds.shape[0] == 2:
        sigma_pts = [None]
    elif bounds.shape[0] == 3:
        sigma_pts = np.linspace(bounds[2,0], bounds[2,1],
                                num_pts_per_sigma)
    elif bounds.shape[0] == 4:
        sigma1 = np.linspace(bounds[2,0], bounds[2,1],
                                num_pts_per_sigma)
        sigma2 = np.linspace(bounds[3,0], bounds[3,1],
                                num_pts_per_sigma)
        sigma1, sigma2 = np.meshgrid(sigma1, sigma2)
        sigma_pts = np.array((sigma1.ravel(), sigma2.ravel())).T
    else:
        raise ValueError("Grid search is only applicable for "
                    "kernels with <= 4 hyperparameters.")
    scoregrid = np.zeros((len(sigma_pts)))
    return sigma_pts, scoregrid
