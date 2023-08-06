"""Describes the xGPRegression class.

The xGPRegression class provides the tools needed to fit a regression
model and make predictions for new datapoints. It inherits from
GPModelBaseclass.
"""
import warnings

try:
    import cupy as cp
    import cupyx as cpx
    from .preconditioners.cuda_randomized_cg_preconditioner import CudaRandomizedPreconditioner
except:
    print("CuPy not detected. xGPR will run in CPU-only mode.")
import numpy as np
from scipy.linalg import cho_solve

from .constants import constants
from .regression_baseclass import GPRegressionBaseclass
from .preconditioners.randomized_cg_preconditioner import CPURandomizedPreconditioner
from .fitting_toolkit.lbfgs_fitting_toolkit import lBFGSModelFit
from .fitting_toolkit.sgd_fitting_toolkit import sgdModelFit
from .fitting_toolkit.ams_grad_toolkit import amsModelFit
from .optimizers.lb_optimizer import shared_hparam_search

from cpu_cg import CPU_ConjugateGrad
from gpu_cg import GPU_ConjugateGrad



class xGPRegression(GPRegressionBaseclass):
    """A subclass of GPRegressionBaseclass that houses methods
    unique to regression problems. It does not have
    any attributes unique to it aside from those
    of the parent class."""

    def __init__(self, training_rffs,
                    fitting_rffs,
                    variance_rffs = 16,
                    kernel_choice="rbf",
                    device = "cpu",
                    kernel_specific_params = constants.DEFAULT_KERNEL_SPEC_PARMS,
                    verbose = True,
                    double_precision_fht = False):
        """The constructor for xGPRegression. Passes arguments onto
        the parent class constructor.

        Args:
            training_rffs (int): The number of random Fourier features
                to use for hyperparameter tuning.
            fitting_rffs (int): The number of random Fourier features
                to use for posterior predictive mean (i.e. the predicted
                value for new datapoints).
            variance_rffs (int): The number of random Fourier features
                to use for posterior predictive variance (i.e. calculating
                uncertainty on predictions). Defaults to 64.
            kernel_choice (str): The kernel that the model will use.
                Must be one of constants.ACCEPTABLE_KERNELS.
                Defaults to 'rbf'.
            device (str): Determines whether calculations are performed on
                'cpu' or 'gpu'. The initial entry can be changed later
                (i.e. model can be transferred to a different device).
                Defaults to 'cpu'.
            kernel_specific_params (dict): Contains kernel-specific parameters --
                e.g. 'matern_nu' for the nu for the Matern kernel, or 'conv_width'
                for the conv1d kernel.
            verbose (bool): If True, regular updates are printed
                during fitting and tuning. Defaults to True.
            double_precision_fht (bool): If False, use single precision floats to generate
                random features. This can increase speed but may result in a slight (usually
                negligible) loss of accuracy.
        """
        super().__init__(training_rffs, fitting_rffs, variance_rffs,
                        kernel_choice, device, kernel_specific_params,
                        verbose, double_precision_fht)
        self.decay_time = 1

    def predict(self, input_x, get_var = True,
            chunk_size = 2000):
        """Generate a predicted value for each
        input datapoint -- and if desired the variance.

        Args:
            input_x (np.ndarray): The input data. Should be a 2d numpy
                array (if non-convolution kernel) or 3d (if convolution
                kernel).
            get_var (bool): If True, return (predictions, variance).
                If False, return predictions. Defaults to True.
            chunk_size (int): The number of datapoints to process at
                a time. Lower values limit memory consumption. Defaults
                to 2000.

        Returns:
            If get_var is True, returns (predictions, variance). If False,
            returns predictions. Both are numpy arrays of length N
            for N datapoints.

        Raises:
            ValueError: If the dimesionality or type of the input does
                not match what is expected, or if the model has
                not yet been fitted, a ValueError is raised.
        """
        xdata = self._pre_prediction_checks(input_x, get_var)
        preds, var = [], []
        for i in range(0, xdata.shape[0], chunk_size):
            cutoff = min(i + chunk_size, xdata.shape[0])
            xfeatures = self.kernel.transform_x(xdata[i:cutoff, :])
            preds.append((xfeatures * self.weights[None, :]).sum(axis = 1))
            if get_var:
                xfeatures = xfeatures[:,:self.variance_rffs]
                pred_var = (self.var @ xfeatures.T).T
                pred_var = (xfeatures * pred_var).sum(axis=1)
                var.append(pred_var)

        if self.device == "gpu":
            preds = cp.asnumpy(cp.concatenate(preds))
        else:
            preds = np.concatenate(preds)
        if not get_var:
            return preds * self.trainy_std + self.trainy_mean
        if self.device == "gpu":
            var = cp.asnumpy(cp.concatenate(var))
            mempool = cp.get_default_memory_pool()
            mempool.free_all_blocks()
        else:
            var = np.concatenate(var)
        return preds * self.trainy_std + self.trainy_mean, var * self.trainy_std



    def _pre_prediction_checks(self, input_x, get_var):
        """Checks the input data to predict_scores to ensure validity.

        Args:
            input_x (np.ndarray): A numpy array containing the input data.
            get_var (bool): Whether a variance calculation is desired.

        Returns:
            x_array: A cupy array (if self.device is gpu) or a reference
                to the unmodified input array otherwise.

        Raises:
            ValueError: If invalid inputs are supplied,
                a detailed ValueError is raised to explain.
        """
        x_array = input_x
        if self.kernel is None:
            raise ValueError("Model has not yet been successfully fitted.")
        if not self.kernel.validate_new_datapoints(input_x):
            raise ValueError("The input has incorrect dimensionality.")
        #TODO: Add proper variance calc for linear kernel.
        if self.var is None and get_var:
            raise ValueError("Variance was requested but suppress_var "
                    "was selected when fitting or a linear kernel was "
                    "used, meaning that variance has not been generated.")
        if self.device == "gpu":
            mempool = cp.get_default_memory_pool()
            mempool.free_all_blocks()
            x_array = cp.asarray(input_x)

        return x_array


    def get_hyperparams(self):
        """Simple helper function to return hyperparameters if the model
        has already been tuned or fitted."""
        if self.kernel is None:
            return None
        return self.kernel.get_hyperparams()


    def build_preconditioner(self, dataset, max_rank = 512,
                        preset_hyperparams = None, random_state = 123,
                        method = "srht"):
        """Tries to build a randomized Nystrom
        preconditioner. The resulting preconditioner object
        can be supplied to fit and used for CG, L-BFGS, SGD etc.

        Args:
            dataset: A Dataset object.
            max_rank (int): The maximum rank for the preconditioner, which
                uses a low-rank approximation to the matrix inverse. Larger
                numbers mean a more accurate approximation and thus reduce
                the number of iterations, but make the preconditioner more
                expensive to construct.
            preset_hyperparams: Either None or a numpy array. If None,
                hyperparameters must already have been tuned using one
                of the tuning methods (e.g. tune_hyperparams_bayes_bfgs).
                If supplied, must be a numpy array of shape (N, 2) where
                N is the number of hyperparams for the kernel in question.
            random_state (int): Seed for the random number generator.
            method (str): one of "srht" or "gauss". srht is MUCH faster for
                large datasets. gauss is faster for small datasets.

        Returns:
            preconditioner: An object of classes CudaRandomizedPreconditioner,
                CudaClassicNystromPreconditioner, or CPURandomizedPreconditioner.
                If preconditioner construction fails, None is returned and a
                warning is issued.
            achieved_ratio (float): The min eigval of the preconditioner over
                lambda, the noise hyperparameter shared between all kernels.
                This value has decent predictive value for assessing how
                well the preconditioner is likely to perform.

        """
        self._run_fitting_prep(dataset, random_state, preset_hyperparams)

        if self.device == "gpu":
            preconditioner = CudaRandomizedPreconditioner(self.kernel.get_lambda(), self.verbose)
        else:
            preconditioner = CPURandomizedPreconditioner(self.kernel.get_lambda(), self.verbose)

        failure = preconditioner.prep_operator(self.kernel,
                            dataset, self.kernel.get_num_rffs(),
                            max_rank, random_state, method)
        achieved_ratio = preconditioner.achieved_ratio

        #It is possible (though extremely rare) for preconditioner construction
        #to fail. Have not yet encountered this situation, but we have this here
        #in case.
        if failure:
            warnings.warn("Preconditioner construction failed! Try using a "
                    "smaller value for max_rank.")
            print("Preconditioner construction failed! Try using a smaller "
                    "value for max_rank.")
            return None, 0.0
        if self.verbose:
            print(f"Preconditioner rank: {preconditioner.get_rank()}")
        if self.device == "gpu":
            mempool = cp.get_default_memory_pool()
            mempool.free_all_blocks()
        return preconditioner, achieved_ratio


    def _calc_weights_exact(self, dataset):
        """Calculates the weights when fitting the model using
        matrix decomposition. Exact and fast for small numbers
        of random features but poor scaling.

        Args:
            dataset: Either OnlineDataset or OfflineDataset,
                containing the information on the dataset we
                are fitting.

        Returns:
            weights: A cupy or numpy array of shape (M) for M
                random features.
        """
        z_trans_z, z_trans_y, _ = self._calc_design_mat(dataset)
        lambda_p = self.kernel.get_hyperparams(logspace=False)[0]
        z_trans_z.flat[::z_trans_z.shape[0]+1] += lambda_p**2
        _, weights = self._direct_weight_calc(z_trans_z, z_trans_y)
        return weights


    def _calc_weights_cg(self, dataset, cg_tol = 1e-4, max_iter = 500,
                        preconditioner = None):
        """Calculates the weights when fitting the model using
        preconditioned CG. Good scaling but slower for small
        numbers of random features.

        Args:
            dataset: Either OnlineDataset or OfflineDataset.
            cg_tol (float): The threshold below which cg is deemed to have
                converged. Defaults to 1e-5.
            max_iter (int): The maximum number of iterations before
                CG is deemed to have failed to converge.
            preconditioner: Either None or a valid Preconditioner (e.g.
                CudaRandomizedPreconditioner, CPURandomizedPreconditioner
                etc). If None, no preconditioning is used. Otherwise,
                the preconditioner is used for CG. The preconditioner
                can be built by calling self.build_preconditioner
                with appropriate arguments.
            starting_guess: Either None or a cupy or numpy array containing
                starting guess values for the weights. Defaults to None.

        Returns:
            weights: A cupy or numpy array of shape (M) for M
                random features.
            n_iter (int): The number of CG iterations.
            losses (list): The loss on each iteration; for diagnostic
                purposes.
        """
        if self.device == "gpu":
            cg_operator = GPU_ConjugateGrad(self.kernel.get_lambda(), self.kernel.get_num_rffs())
        else:
            cg_operator = CPU_ConjugateGrad(self.kernel.get_lambda(), self.kernel.get_num_rffs())

        z_trans_y = cg_operator.get_zTy(dataset, self.kernel)

        weights, converged, n_iter, losses = cg_operator.fit(dataset, self.kernel,
                preconditioner, z_trans_y, max_iter, cg_tol, self.verbose)
        if not converged:
            warnings.warn("Conjugate gradients failed to converge! Try refitting "
                        "the model with updated settings.")

        if self.verbose:
            print(f"CG iterations: {n_iter}")
        return weights, n_iter, losses



    def _calc_weights_lbfgs(self, fitting_dataset, tol, max_iter = 500):
        """Calculates the weights when fitting the model using
        L-BFGS. Only recommended for small datasets.

        Args:
            fitting_dataset: An OnlineDataset or OfflineDataset with
                the training data to be fitted.
            tol (float): The threshold for convergence.
            max_iter (int): The maximum number of L-BFGS iterations.
            random_state (int): Seed for the random number generator.

        Returns:
            weights: A cupy or numpy array (depending on self.device)
                containing the resulting weights from fitting.
            niter (int): The number of function evaluations required
                to obtain this set of weights.
        """
        model_fitter = lBFGSModelFit(fitting_dataset, self.kernel,
                    self.device, self.verbose)
        weights = model_fitter.fit_model_lbfgs(max_iter, tol)
        n_iter = model_fitter.get_niter()
        return weights, n_iter




    def _calc_weights_sgd(self, fitting_dataset, tol, max_iter = 50,
            preconditioner = None, manual_lr = None):
        """Calculates the weights when fitting the model using
        stochastic variance reduction gradient descent, preferably
        with preconditioning (although can also function without).
        Excellent scaling, but a little less accurate than CG.

        Args:
            fitting_dataset: An OnlineDataset or OfflineDataset with
                the training data to be fitted.
            tol (float): The threshold for convergence.
            max_iter (int): The maximum number of epochs.
            preconditioner: Either None or a valid Preconditioner object.
            manual_lr (float): Either None or a float. If not None, this
                is a user-specified initial learning rate. If None, find
                a good initial learning rate using autotuning.

        Returns:
            weights: A cupy or numpy array (depending on self.device)
                containing the resulting weights from fitting.
            niter (int): The number of function evaluations required
                to obtain this set of weights.
            losses (list): A list of losses at each iteration.
        """
        model_fitter = sgdModelFit(self.kernel.get_lambda(), self.device, self.verbose)
        weights, losses = model_fitter.fit_model(fitting_dataset,
                    self.kernel, tol = tol, max_epochs = max_iter,
                    preconditioner = preconditioner, manual_lr = manual_lr)
        n_iter = model_fitter.get_niter()
        return weights, n_iter, losses


    def _calc_weights_ams(self, fitting_dataset, tol, max_iter = 50):
        """Calculates the weights when fitting the model using
        AMSGrad. Use for testing purposes only -- this is not currently
        competitive with our other methods on tough problems.

        Args:
            fitting_dataset: An OnlineDataset or OfflineDataset with
                the training data to be fitted.
            tol (float): The threshold for convergence.
            max_iter (int): The maximum number of epochs.

        Returns:
            weights: A cupy or numpy array (depending on self.device)
                containing the resulting weights from fitting.
            niter (int): The number of function evaluations required
                to obtain this set of weights.
        """
        model_fitter = amsModelFit(self.kernel.get_lambda(), self.device, self.verbose)
        weights, losses = model_fitter.fit_model(fitting_dataset,
                    self.kernel, tol = tol, max_epochs = max_iter)
        n_iter = model_fitter.get_niter()
        return weights, n_iter, losses



    def _calc_variance(self, dataset):
        """Calculates the var matrix used for calculating
        posterior predictive variance on new datapoints. We
        only ever use closed-form matrix-decomposition based
        calculations here since the variance does not need to
        be approximated as accurately as the posterior predictive
        mean, so we can restrict the user to a smaller number of
        random features (defined in constants.constants).

        Args:
            dataset: Either an OnlineDataset or an OfflineDataset containing
                the data that needs to be fitted.

        Returns:
            var: A cupy or numpy array of shape (M, M) where M is the
                number of random features.
        """
        if self.verbose:
            print("Estimating variance...")
        #This is a very naughty hack.
        #TODO: Add a proper variance calc for linear.
        if self.kernel_choice == "Linear":
            return None
        z_trans_z = self._calc_var_design_mat(dataset)
        lambda_ = self.kernel.get_lambda()
        z_trans_z.flat[::z_trans_z.shape[0]+1] += lambda_**2
        if self.device == "cpu":
            var = np.linalg.pinv(z_trans_z)
        else:
            var = cp.linalg.pinv(z_trans_z)
        if self.verbose:
            print("Variance estimated.")
        return var


    def _direct_weight_calc(self, chol_z_trans_z, z_trans_y):
        """Calculates the cholesky decomposition of (z^T z + lambda)^-1
        and then uses this to calculate the weights as (z^T z + lambda)^-1 z^T y.
        This exact calculation is only suitable for < 10,000 random features or so;
        cholesky has O(M^3) scaling.

        Args:
            z_trans_z: An M x M cupy or numpy matrix where M is the number of
                random features formed from z^T z when z is the random features
                generated for raw input data X.
            z_trans_y: A length M cupy or numpy array where M is the number of
                random features, formed from z^T y.

        Returns:
            chol_z_trans_z: The cholesky decomposition of z_trans_z. An M x M
                cupy or numpy matrix.
            weights: A length M cupy or numpy array containing the weights.
        """
        lambda_p = self.kernel.get_hyperparams(logspace=False)[0]
        chol_z_trans_z.flat[::chol_z_trans_z.shape[0]+1] += lambda_p**2
        if self.device == "cpu":
            chol_z_trans_z = np.linalg.cholesky(chol_z_trans_z)
            weights = cho_solve((chol_z_trans_z, True), z_trans_y)
        else:
            chol_z_trans_z = cp.linalg.cholesky(chol_z_trans_z)
            weights = cpx.scipy.linalg.solve_triangular(chol_z_trans_z,
                            z_trans_y, lower=True)
            weights = cpx.scipy.linalg.solve_triangular(chol_z_trans_z.T,
                            weights, lower=False)
        return chol_z_trans_z, weights



    def _calc_design_mat(self, dataset, multiply_by_beta = True):
        """Calculates the z_trans_z (z^T z) matrix where Z is the random
        features generated from raw input data X. Also generates
        y^T y and z^T y.

        Args:
            dataset: An OnlineDataset or OfflineDataset object storing
                the data we will use.
            multiply_by_beta (bool): If False, do not multiply the random
                features by beta (the kernel amplitude) when they are generated.
                This is useful for some gridsearch procedures. Defaults to
                True.

        Returns:
            z_trans_z: The cupy or numpy matrix resulting from z^T z. Will
                be shape M x M for M random features.
            z_trans_y: The cupy or numpy length M array resulting from
                z^T y for M random features.
            y_trans_y (float): The result of the dot product of y with itself.
                Used for some marginal likelihood calculations.
        """
        num_rffs = self.kernel.get_num_rffs()
        if self.device == "cpu":
            z_trans_z, z_trans_y = np.zeros((num_rffs, num_rffs)), np.zeros((num_rffs))
        else:
            z_trans_z = cp.zeros((num_rffs, num_rffs))
            z_trans_y = cp.zeros((num_rffs))
        y_trans_y = 0.0
        for xdata, ydata in dataset.get_chunked_data():
            xfeatures = self.kernel.transform_x(xdata, multiply_by_beta =
                        multiply_by_beta, pretransformed = dataset.pretransformed)
            z_trans_y += xfeatures.T @ ydata
            z_trans_z += xfeatures.T @ xfeatures
            y_trans_y += ydata.T @ ydata
        return z_trans_z, z_trans_y, float(y_trans_y)


    def _calc_var_design_mat(self, dataset):
        """Calculates the z_trans_z (z^T z) matrix where Z is the random
        features generated from raw input data X, for calculating
        variance only (since in this case we only use up to
        self.variance_rffs of the features generated).

        Args:
            dataset: An OnlineDataset or OfflineDataset object storing
                the data we will use.

        Returns:
            z_trans_z: The cupy or numpy matrix resulting from z^T z. Will
                be shape M x M for M random features.
        """
        num_rffs = self.variance_rffs
        if self.device == "cpu":
            z_trans_z = np.zeros((num_rffs, num_rffs))
        else:
            z_trans_z = cp.zeros((num_rffs, num_rffs))
        for xdata in dataset.get_chunked_x_data():
            xfeatures = self.kernel.transform_x(xdata,
                        pretransformed = dataset.pretransformed)
            xfeatures = xfeatures[:,:num_rffs]
            z_trans_z += xfeatures.T @ xfeatures
        return z_trans_z


    def calc_gradient_terms(self, dataset):
        """Calculates terms needed for the gradient calculation.

        Args:
            dataset: An OnlineDataset or OfflineDataset with the
                raw data we need for these calculations.

        Returns:
            z_trans_z: The M x M cupy or numpy matrix for M random features.
            z_trans_y: The length M cupy or numpy array for M random features.
            y_trans_y (float): The dot product of y with itself.
            dz_dsigma_ty (array): Derivative w/r/t kernel-specific hyperparams times y.
            inner_deriv (array): Derivative for the log determinant portion of the NMLL.
        """
        num_rffs = self.kernel.get_num_rffs()
        hparams = self.kernel.get_hyperparams()
        if self.device == "cpu":
            z_trans_z = np.zeros((num_rffs, num_rffs))
            z_trans_y = np.zeros((num_rffs))
            dz_dsigma_ty = np.zeros((num_rffs, hparams.shape[0] - 2))
            inner_deriv = np.zeros((num_rffs, num_rffs,
                                    hparams.shape[0] - 2))
            transpose = np.transpose
        else:
            z_trans_z = cp.zeros((num_rffs, num_rffs))
            z_trans_y = cp.zeros((num_rffs))
            dz_dsigma_ty = cp.zeros((num_rffs, hparams.shape[0] - 2))
            inner_deriv = cp.zeros((num_rffs, num_rffs,
                                    hparams.shape[0] - 2))
            transpose = cp.transpose

        y_trans_y = 0

        for xdata, ydata in dataset.get_chunked_data():
            xfeatures, dz_dsigma = self.kernel.kernel_specific_gradient(xdata)
            z_trans_y += xfeatures.T @ ydata
            z_trans_z += xfeatures.T @ xfeatures
            y_trans_y += ydata.T @ ydata

            for i in range(dz_dsigma.shape[2]):
                dz_dsigma_ty[:,i] += dz_dsigma[:,:,i].T @ ydata
                inner_deriv[:,:,i] += dz_dsigma[:,:,i].T @ xfeatures

        inner_deriv += transpose(inner_deriv, (1,0,2))
        return z_trans_z, z_trans_y, float(y_trans_y), dz_dsigma_ty, inner_deriv






    def exact_nmll(self, hyperparams, dataset, verbose=False, suppress_warnings = False):
        """Calculates the exact negative marginal log likelihood (the model
        'score') using matrix decompositions. Fast for small numbers of random
        features but poor scaling to larger numbers.

        Args:
            hyperparams (np.ndarray): A numpy array containing the new
                set of hyperparameters that should be assigned to the kernel.
            dataset: An OnlineDataset or OfflineDataset containing the raw
                data we will use for this evaluation.
            verbose (bool): If True, print an update.

        Returns:
            negloglik (float): The negative marginal log likelihood for the
                input hyperparameters.
        """
        self.kernel.set_hyperparams(hyperparams, logspace=True)
        nsamples = dataset.get_ndatapoints()
        z_trans_z, z_trans_y, y_trans_y = self._calc_design_mat(dataset)
        if self.device == "cpu":
            diagfunc, logfunc = np.diag, np.log
        else:
            diagfunc, logfunc = cp.diag, cp.log

        lambda_p = self.kernel.get_lambda()
        #Direct weight calculation may fail IF the hyperparameters supplied
        #lead to a singular design matrix. This is rare, but be prepared to
        #handle if this problem is encountered.
        try:
            chol_z_trans_z, weights = self._direct_weight_calc(z_trans_z, z_trans_y)
        except:
            if not suppress_warnings:
                warnings.warn("Near-singular matrix encountered when calculating score for "
                    f"hyperparameters {hyperparams}.")
            return constants.DEFAULT_SCORE_IF_PROBLEM
        negloglik = (-0.5 / lambda_p**2) * (z_trans_y.T @ weights)
        negloglik += logfunc(diagfunc(chol_z_trans_z)).sum()
        negloglik += 0.5 * y_trans_y / lambda_p**2
        negloglik += (nsamples - z_trans_z.shape[0]) * logfunc(lambda_p)
        negloglik += nsamples * 0.5 * logfunc(2 * np.pi)
        negloglik = float(negloglik)
        #Direct weight calculation may fail IF the hyperparameters supplied
        #lead to a singular design matrix. This is rare, but be prepared to
        #handle if this problem is encountered.
        if np.isnan(negloglik):
            if not suppress_warnings:
                warnings.warn("Near-singular matrix encountered when calculating score for "
                    f"hyperparameters {hyperparams}.")
            return constants.DEFAULT_SCORE_IF_PROBLEM
        if verbose:
            print("Evaluated NMLL.")
        return negloglik



    def exact_nmll_gradient(self, hyperparams, dataset, print_update = False):
        """Calculates the gradient of the negative marginal log likelihood w/r/t
        the hyperparameters for a specified set of hyperparameters using
        exact methods (matrix decompositions). Fast for small numbers of
        random features, impractical for large.

        Args:
            hyperparams (np.ndarray): The set of hyperparameters at which
                to calculate the gradient.
            dataset: An Online or OfflineDataset containing the raw data
                we will use for this evaluation.
            print_update (bool): If True, print an update during this
                calculation. Defaults to False.

        Returns:
            negloglik (float): The negative marginal log likelihood.
            grad (np.ndarray): The gradient of the NMLL w/r/t the hyperparameters.
        """
        init_hparams = self.kernel.get_hyperparams()
        self.kernel.set_hyperparams(hyperparams, logspace=True)
        hparams = self.kernel.get_hyperparams(logspace=False)

        if self.device == "cpu":
            diagfunc, logfunc = np.diag, np.log
        else:
            _ = cpx.seterr(linalg="raise")
            diagfunc, logfunc = cp.diag, cp.log

        if print_update and self.verbose:
            print("Evaluating gradient...")

        nsamples = dataset.get_ndatapoints()
        z_trans_z, z_trans_y, y_trans_y, dz_dsigma_ty, inner_deriv = \
                        self.calc_gradient_terms(dataset)
        lambda_p, beta = hparams[0], hparams[1]
        grad = np.zeros((hparams.shape[0]))

        #Try-except here since very occasionally, optimizer samples a really
        #terrible set of hyperparameters that with numerical error has resulted in a
        #non-positive-definite design matrix. TODO: Find a good workaround to
        #avoid this whole problem.
        try:
            chol_z_trans_z, weights, grad[0], grad[1] = self.kernel.shared_hparams_reg_grad(
                        z_trans_z, z_trans_y, y_trans_y, lambda_p, beta, nsamples)
        except Exception as e:
            return 1e40, hyperparams - init_hparams

        grad[2:] = self.kernel.nonshared_hparams_reg_grad(chol_z_trans_z, weights,
                            dz_dsigma_ty, inner_deriv, lambda_p, hparams)
        negloglik = (-0.5 / lambda_p**2) * (z_trans_y.T @ weights)
        negloglik += logfunc(diagfunc(chol_z_trans_z)).sum()
        negloglik += 0.5 * y_trans_y / lambda_p**2
        negloglik += (nsamples - chol_z_trans_z.shape[0]) * logfunc(lambda_p)
        negloglik += nsamples * 0.5 * logfunc(2 * np.pi)
        #Same problem as above, only occasionally the LAPACK routines return
        #nan instead of raising an error.
        if np.isnan(negloglik):
            return 1e40, hyperparams - init_hparams
        return float(negloglik), grad




    def gridsearch_nmll(self, sigma_vals, dataset, bounds, n_pts_per_dim = 40,
                        min_eigval = 1e-6):
        """This specialized grisearch procedure is best used for <= 5000
        random features since it requires an eigendecomposition of a Hermitian
        matrix. It makes up for this drawback by being able to evaluate many
        values of lambda and beta (shared hyperparameters) for each
        eigendecomposition. This reduces a 4d or 3d problem to a 2d or 1d
        problem and thereby make it highly tractable.

        Args:
            sigma_vals: Either None or a numpy array of length C for
                C kernel specific hyperparameters.
            dataset: An OnlineDataset or OfflineDataset containing the raw data.
            bounds (np.ndarray): A 2 x 2 numpy array where [0,:] is the boundaries
                for the lambda shared hyperparameter and [1,:] is the boundaries
                for the beta shared hyperparameter.
            n_pts_per_dim (int): The number of grid points per each shared hyperparameter.
                Too many can cause large memory consumption; too few can result in
                missing the global minimum. 40 is a reasonable default that should be
                increased if the size of the optimization bounds is expanded considerably,
                but can also be decreased if the search is over a small neighborhood.
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
        if sigma_vals is not None:
            hparams = self.kernel.get_hyperparams(logspace=True)
            hparams[2:] = sigma_vals
            self.kernel.set_hyperparams(hparams, logspace=True)
        z_trans_z, z_trans_y, y_trans_y = self._calc_design_mat(dataset,
                                        multiply_by_beta = False)
        if self.device == "cpu":
            eigh = np.linalg.eigh
        else:
            eigh = cp.linalg.eigh

        nsamples = dataset.get_ndatapoints()

        try:
            eigvals, eigvec = eigh(z_trans_z)
        except:
            raise ValueError("A fatal numerical error occured during eigendecomposition. "
                    "Generally this issue is caused by either single precision fht or "
                    "extreme hyperparameter values."
                    "Please use a more limited boundary region for hyperparameter optimization, "
                    f"or turn off single_precision_tuning if currently enabled. Problem "
                    f"encountered for sigma values {sigma_vals}.")
        del z_trans_z
        z_trans_y = eigvec.T @ z_trans_y
        del eigvec
        return shared_hparam_search(z_trans_y, eigvals, nsamples, y_trans_y, self.device,
                                bounds, n_pts_per_dim, min_eigval = min_eigval)
