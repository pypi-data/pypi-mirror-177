"""Contains the tools needed to perform adam stochastic gradient descent.
Note that in general this method achieves inferior results and we do
not recommend it except as a necessary evil for very large datasets
(or without some substantial modifications)."""
import copy
import numpy as np

from ..data_handling.minibatch_data_handler import MinibatchDataset


def stochastic_tuning(dataset, minibatch_size, n_epochs,
                    learn_rate, random_state, init_hyperparams,
                    num_restarts, bounds, tol,
                    cost_fun, verbose = True):
    """Wraps the adam_optimizer and stochastic_optimizer, running whichever caller
    requests, and runs num_restarts, saving the best result.

    Args:
        dataset: An OnlineDataset or OfflineDataset with the raw data we will
            use for tuning.
        minibatch_size (int): The minibatch size.
        n_epochs (int): The number of epochs per restart.
        learn_rate (float): The learning rate parameter for the Adam algorithm.
            For the SVRGD algorithm, this is used as an initial learning rate
            which is then updated.
        random_state (int): The seed for the random number generator.
        init_hyperparams (np.ndarray): The starting point for optimization.
            If None, num_restarts random locations are picked. If not None,
            must be a numpy array. If not None, num_restarts is ignored
            and a single restart is conducted with the starting point.
        num_restarts (int): Adam optimization is restarted num_restarts times
            UNLESS init_hyperparams is not None, in which case it is conducted
            once from that starting point.
        bounds (np.ndarray): The boundaries of the hyperparameter optimization.
            Must be of shape N x 2 for N hyperparameters.
        tol (float): The convergence threshold for optimization.
        cost_fun: A function that evaluates the negative marginal log likelihood
            AND its gradient for a given set of input hyperparameters and an
            input MinibatchDataset object.
        verbose (bool): If True, regular updates are printed during optimization.

    Returns:
        best_params (np.ndarray): The best hyperparameters obtained.
        all_costs (list): A list of the best NMLL achieved on each restart.
        net_iterations (int): The total number of iterations across all restarts.
    """
    rng = np.random.default_rng(random_state)
    best_cost, net_iterations, best_params = np.inf, 0, None
    all_costs = []
    for i in range(num_restarts):
        if init_hyperparams is not None:
            init_hparams = init_hyperparams
        else:
            init_hparams = rng.uniform(low=bounds[:,0], high=bounds[:,1],
                    size=bounds.shape[0])
        dataset.reset_index()
        #If a non-positive definite matrix is encountered, we've stumbled
        #across a really bad set of hyperparameters. This doesn't mean we
        #need to stop dead in our tracks -- it means we need to move to
        #the next restart and print some kind of notification to user.
        try:
            hyperparams, cost, iterations = adam_optimizer(cost_fun,
                    init_hparams, dataset,
                    bounds, minibatch_size,
                    n_epochs, learn_rate,
                    verbose, tol)
        except:
            if verbose:
                print("Failure / non-positive definite matrix on stochastic "
                        "optimization attempt. Retrying...")
            continue
        net_iterations += iterations
        dataset.reset_index()
        if cost < best_cost:
            best_cost = copy.copy(cost)
            best_params = copy.deepcopy(hyperparams)
        all_costs.append(cost)
        if init_hyperparams is not None:
            break
    if best_params is None:
        raise ValueError("No stochastic optimization attempt succeeded.")
    return best_params, all_costs, net_iterations



def adam_optimizer(cost_fun, init_param_vals, dataset, bounds,
                        minibatch_size = 2000,
                        n_epochs = 1, learn_rate = 0.001,
                        verbose = True, tol = 1e-3):
    """Performs a single round of Adam stochastic gradient descent optimization.

    Args:
        cost_fun: A function that evaluates the negative marginal log likelihood
            AND its gradient for a given set of input hyperparameters and an
            input MinibatchDataset object.
        init_param_vals (np.ndarray): A starting point for this round of
            optimization.
        dataset: An OnlineDataset or OfflineDataset with the raw data we will
            use for tuning.
        bounds (np.ndarray): The boundaries of the hyperparameter optimization.
            Must be of shape N x 2 for N hyperparameters.
        minibatch_size (int): The minibatch size.
        n_epochs (int): The number of epochs per restart.
        learn_rate (float): The learning rate parameter for the Adam algorithm.
        verbose (bool): If True, regular updates are printed during optimization.
        tol (float): The convergence threshold for optimization.

    Returns:
        params (np.ndarray): The best hyperparameters obtained.
        cost (float): The estimated cost for the last value.
        iteration (int): The number of iterations performed.
    """
    optim_eps = 1e-8
    beta1, beta2, beta1_t, beta2_t = 0.9, 0.999, 0.9, 0.999
    params = np.copy(init_param_vals)
    most_recent_params, most_recent_costs = [], []

    moment1, moment2 = np.zeros((params.shape[0])), \
                np.zeros((params.shape[0]))
    shift_tracker = []
    epoch, iteration = 0, 0
    while epoch < n_epochs:
        xbatch, ybatch, end_epoch = dataset.get_next_minibatch(minibatch_size)
        mbatch = MinibatchDataset(xbatch, ybatch,
                            dataset.pretransformed)

        cost, grad = cost_fun(params, mbatch, print_update=False)
        grad = grad / xbatch.shape[0]
        moment1 = beta1 * moment1 + (1 - beta1) * grad
        moment2 = beta2 * moment2 + (1 - beta2) * grad**2
        bias_corr_moment1 = moment1 / (1 - beta1_t)
        bias_corr_moment2 = moment2 / (1 - beta2_t)
        params = params - learn_rate * bias_corr_moment1 / (np.sqrt(bias_corr_moment2) +
                    optim_eps)
        params = np.clip(params, a_min=bounds[:,0], a_max=bounds[:,1])
        most_recent_costs.append(cost)
        most_recent_params.append(params)
        if len(most_recent_params) > 20:
            del most_recent_params[0]
            del most_recent_costs[0]
        beta1_t = beta1_t * beta1
        beta2_t = beta2_t * beta2

        shift_tracker.append(cost)
        iteration += 1
        if end_epoch:
            epoch += 1
            if verbose:
                print("Epoch ended")

        if len(shift_tracker) > 4:
            max_shift = np.max(np.abs(np.diff(shift_tracker[-4:])))
            if verbose:
                if iteration % 20 == 0:
                    print(f"Iteration {iteration} complete")
                if iteration % 10 == 0:
                    print(f"Cost: {shift_tracker[-1]}")
            if max_shift < tol:
                print(max_shift)
                break
    most_recent_params = np.mean(np.stack(most_recent_params), axis=0)
    return most_recent_params, np.mean(most_recent_costs), iteration
