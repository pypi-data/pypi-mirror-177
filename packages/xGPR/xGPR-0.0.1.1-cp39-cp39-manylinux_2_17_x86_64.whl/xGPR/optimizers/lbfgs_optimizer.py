"""Describes the lbfgs_optimizer function for performing L-BFGS
based hyperparameter optimization."""
import numpy as np
from scipy.optimize import minimize

def lbfgs_optimizer(dataset, cost_fun, bounds,
                    random_state, n_restarts, max_iter,
                    init_hyperparams = None,
                    verbose=True):
    """Performs n_restarts of lbfgs hyperparameter optimization.

    Args:
        dataset: An OnlineDataset or OfflineDataset containing the
            raw data.
        cost_fun: A function that calculates and returns the
            negative marginal log-likelihood (a float) and the
            gradient (an np.ndarray) for a given set of input
            hyperparameters and an OnlineDataset or OfflineDataset
            object.
        random_state (int): A seed for the random number generator.
        n_restarts (int): The number of times to restart optimization.
            If init_hyperparams is not None, this is ignored and a
            single restart is performed.
        max_iter (int): The maximum number of iterations per restart.
        init_hyperparams (np.ndarray): Either None or a length N
            numpy array containing the starting point for optimization.
            If not None, only a single restart is performed. If None,
            n_restarts random starting points are used.
        verbose (bool): If True, regular updates are printed during
            optimization.
    """
    best_x, best_score, all_scores = None, np.inf, []
    net_iterations = []
    bounds_tuples = list(map(tuple, bounds))
    best_x = None
    if verbose:
        print("Now beginning L-BFGS minimization.")
    init_params = get_starting_params(init_hyperparams, random_state,
                        bounds)
    for iteration in range(n_restarts):
        #If a non-positive definite matrix is encountered, we've stumbled
        #across a really bad set of hyperparameters. This doesn't mean we
        #need to stop dead in our tracks -- it means we need to move to
        #the next restart and print some kind of notification to user.
        try:
            res = minimize(cost_fun, options={"maxiter":max_iter},
                    x0 = init_params, args = (dataset,True),
                    jac = True, bounds = bounds_tuples)
        except Exception as e:
            print(e)
            if verbose:
                print("Error encountered "
                        "during l-bfgs minimization. Retrying...")
            continue
        if res.fun < best_score:
            best_x = res.x
            best_score = res.fun
        all_scores.append(res.fun)
        net_iterations.append(res.nfev)
        if verbose:
            print(f"Restart {iteration} completed. "
                    f"Best score is {best_score}.")
        init_params = get_starting_params(init_hyperparams,
                            random_state + iteration, bounds)
    return best_x, all_scores, sum(net_iterations)



def get_starting_params(init_hyperparams, random_state, bounds):
    """Either returns the input hyperparameters if not None,
    or generates a new set of random hyperparameters as a starting
    point for optimization."""
    rng = np.random.default_rng(random_state)
    if init_hyperparams is None:
        return rng.uniform(low=bounds[:,0], high=bounds[:,1],
                    size=bounds.shape[0])
    else:
        return init_hyperparams
