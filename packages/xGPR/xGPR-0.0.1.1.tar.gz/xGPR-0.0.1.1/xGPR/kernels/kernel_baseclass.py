"""The baseclass for all other standard kernels and for SORFKernelBaseclass.

KernelBaseclass houses methods and attributes used by all kernels, including
for resetting the device, calculating the gradient for hyperparameters that
all kernels have etc. It also includes some abstractmethods to ensure
each kernel exposes the same methods to the model classes.
"""
import abc
from abc import ABC
import warnings

import numpy as np
try:
    import cupy as cp
except:
    pass
from .cho_solvers import cpu_cho_calcs, gpu_cho_calcs, cpu_cho_solver, gpu_cho_solver


class KernelBaseclass(ABC):
    """The baseclass for all other kernel classes.

    Attributes:
        num_freqs (int): The number of sampled frequencies.
        num_rffs (int): The number of random fourier features. Note that
            this will be the same for most kernels. The exception is "sine-
            cosine kernels", e.g. RBF, Matern, which use both the sine
            and cosine of each feature to generate two separate random
            features. In this case the user-requested num_rffs must
            be an even number and num_rffs will be set equal to this
            value, while num_freqs will be 0.5 * num_features.
        xdim (tuple): The dimensionality of the input. Only elements
            1 and onwards are used -- element 0 is the number of datapoints.
        padded_dims (int): The next largest power of two greater than
            xdim[1], since the Hadamard transform only operates on
            vectors whose length is a power of two.
        device (str): Must be one of 'cpu', 'gpu'. Determines where
            calculations are performed.
        hyperparams (np.ndarray): An array of shape (N) for N hyperparameters.
            Initialized here to None, each child class will set to its
            own defaults.
        bounds (np.ndarray): An array of shape (N, 2) for N hyperparameters
            that determines the optimization bounds for hyperparameter tuning.
            Each kernel has its own defaults. The parent class initializes to
            None, child classes must set this value.
        cho_solver: A reference to either cpu_cho_solver or gpu_cho_solver, as
            appropriate for current device.
        zero_arr: A reference to either np.zeros or cp.zeros, depending on
            self.device. This is for convenience and ensures that child
            classes can call self.zero_arr and get an array appropriate
            for the current device.
        dtype: A reference to either np.float64, np.float32, cp.float32, cp.float64
            depending on self.device and self.double_precision (see below).
        out_type: A reference to either np.float64 or cp.float64 depending on
            device.
        empty: A reference to either np.emtpy or cp.empty depending on self.device.
        double_precision (bool): If True, generate random features in double precision.
            Otherwise, generate as single precision.
    """

    def __init__(self, num_rffs, xdim, double_precision = True,
            sine_cosine_kernel = False):
        """Constructor for the KernelBaseclass.

        Args:
            num_rffs (int): The user-requested number of random Fourier features.
                For sine-cosine kernels (RBF, Matern), this will be saved by the
                class as num_rffs.
            xdim (tuple): The dimensions of the input. Either (N, D) or (N, M, D)
                where N is the number of datapoints, D is number of features
                and M is number of timepoints or sequence elements (convolution
                kernels only).
            double_precision (bool): If True, generate random features in double precision.
                Otherwise, generate as single precision.
            sine_cosine_kernel (bool): If True, the kernel is a sine-cosine kernel,
                meaning it will sample self.num_freqs frequencies and use the sine
                and cosine of each to generate twice as many features
                (self.num_rffs). sine-cosine kernels only accept num_rffs
                that are even numbers.

        Raises:
            ValueError: Raises a ValueError if a sine-cosine kernel is requested
                but num_rffs is not an integer multiple of 2.
        """
        self.double_precision = double_precision
        if sine_cosine_kernel:
            if num_rffs <= 1 or not (num_rffs / 2).is_integer():
                raise ValueError("For sine-cosine kernels (e.g. matern, rbf) "
                        "the number of random fourier features must be an integer "
                        "multiple of two.")
            self.num_freqs = int(num_rffs / 2)
            self.num_rffs = num_rffs
        else:
            self.num_freqs = num_rffs
            self.num_rffs = num_rffs
        self.xdim = xdim
        self.hyperparams = None
        self.bounds = None


    @abc.abstractmethod
    def pretransform_x(self, input_x):
        """Kernel classes must implement a method that performs
        the appropriate first step in random feature generation
        (for most kernels, the SORF operation)."""


    @abc.abstractmethod
    def finish_transform(self, input_x, multiply_by_beta = True):
        """Kernel classes must implement a method that performs
        the appropriate second step in random feature generation
        (for most kernels, the activation function."""

    @abc.abstractmethod
    def kernel_specific_set_device(self, new_device):
        """Kernel classes must implement a method that performs
        any kernel-specific operations needed to switch device
        for the kernel."""


    def check_bounds(self, bounds):
        """Checks a set of bounds provided by the caller to ensure they
        are valid for the selected kernel.

        Args:
            bounds (np.ndarray): A numpy array of shape (N, 2) where N
                is the number of hyperparameters, with bounds as
                (low, high).

        Raises:
            ValueError: A ValueError is raised if the bounds array
                passed is not valid for this kernel.
        """
        if bounds.shape != self.bounds.shape:
            raise ValueError("You have tried to supply a set of bounds "
                "for hyperparameter tuning that do not match the shape "
                "of the bounds for the kernel you have chosen. The bounds "
                "should be a numpy array of shape [n_hyperparams, 2] "
                "where the first column is the low bound, second column "
                "is the high bound.")


    def get_bounds(self, logspace=True):
        """Returns the bounds for hyperparameter optimization.
        Note that we do not make this a property because callers
        may need to specify whether they are using logspace (or not).

        Args:
            logspace (bool): If True, return the log of the boundary
                values, otherwise, return the actual values.

        Returns:
            self.bounds (np.ndarray): A numpy array of shape
                (N, 2) where N is the number of hyperparameters,
                containing either the (low, high) bounds
                or the natural lof of those bounds.
        """
        if logspace:
            return np.log(self.bounds)
        return self.bounds


    def set_bounds(self, bounds, logspace=True):
        """Sets the bounds for hyperparameter optimization.
        Note that we do not make this a property because callers
        may need to specify whether they are using logspace (or not).

        Args:
            bounds (np.ndarray): Must be an array of shape (N, 2) where
                N is the number of hyperparameters, with bounds as
                (low, high).
            logspace (bool): If True, the supplied values are the log
                of the actual bounds.

        Raises:
            ValueError: A ValueError is raised if the bounds array
                passed by caller is invalid for the chosen kernel.
        """
        if self.bounds is not None:
            self.check_bounds(bounds)
        if logspace:
            self.bounds = np.exp(bounds)
        else:
            self.bounds = bounds



    def get_scaling_factors(self):
        """Returns the training set mean and training set std
        attributes. These may be None (if we have not acquired
        them, or are not scaling random features) or may be
        numpy or cupy arrays, depending on current device.
        Note that this function IS NOT CURRENTLY USED.
        Preliminary experiments suggested that scaling
        is sometimes moderately helpful and sometimes
        harmful. As such we have not yet introduced it."""
        return (self.train_mean, self.train_std)


    def set_scaling_factors(self, train_dataset, pretransformed = False,
            scaling_factors = None):
        """This function either sets the scaling factors to those provided,
        or calculates the mean & std of the random features using the
        training set and stores them for future use.
        Note that this function IS NOT CURRENTLY USED.
        Preliminary experiments suggested that scaling
        is sometimes moderately helpful and sometimes
        harmful. As such we have not yet introduced it.

        Args:
            train_dataset: A dataset object for the training set. Will be
                used to calculate self.train_mean and self.train_std if
                scaling_factors is None.
            pretransformed (bool): If True, the data has been pretransformed
                and features saved to disk, otherwise False.
            scaling_factors: Either None or a tuple of (train_mean, train_std)
                where train_mean and train_std are numpy or cupy arrays
                depending on device.

        Raises:
            ValueError: A ValueError is raised if invalid input is supplied.
        """
        if scaling_factors is None:
            self.calculate_scaling_factors(train_dataset, pretransformed)
        else:
            if not isinstance(scaling_factors, tuple):
                raise ValueError("Scaling factors supplied to the "
                    "kernel is not a tuple as expected.")
            if len(scaling_factors) != 2:
                raise ValueError("Tuple of unexpected size supplied "
                        "to kernel as scaling factors.")

            train_mean, train_std = scaling_factors
            if train_mean.shape[0] != self.num_rffs or\
                    train_std.shape[0] != self.num_rffs:
                warnings.warn("Kernel was supplied with scaling factors "
                        "of incorrect shape. Now recalculating scaling "
                        "factors.")
                self.calculate_scaling_factors(train_dataset, pretransformed)
            elif self.device == "gpu":
                self.train_mean = cp.asarray(train_mean)
                self.train_std = cp.asarray(train_std)
            else:
                if not isinstance(train_mean, np.ndarray):
                    self.train_mean = cp.asnumpy(train_mean)
                    self.train_std = cp.asnumpy(train_std)
                else:
                    self.train_mean = train_mean
                    self.train_std = train_std


    def calculate_scaling_factors(self, train_dataset, pretransformed):
        """This function calculates scaling factors (self.train_mean and
        self.train_std).
        Note that this function IS NOT CURRENTLY USED.
        Preliminary experiments suggested that scaling
        is sometimes moderately helpful and sometimes
        harmful. As such we have not yet introduced it.

        Args:
            train_dataset: A dataset object for the training set. Will be
                used to calculate self.train_mean and self.train_std.
            pretransformed (bool): If True, the data has been pretransformed
                and features saved to disk, otherwise False.
        """
        self.train_mean, self.train_std = None, None
        train_mean, train_var = self.zero_arr((self.num_rffs)), \
                self.zero_arr((self.num_rffs))
        ndpoints = 0
        for xdata in train_dataset.get_chunked_x_data():
            xdata = self.transform_x(xdata, pretransformed = pretransformed)
            w_1 = xdata.shape[0] / (xdata.shape[0] + ndpoints)
            w_2 = ndpoints / (xdata.shape[0] + ndpoints)
            w_3 = ndpoints * xdata.shape[0] / (xdata.shape[0] + ndpoints)**2

            xdata_mean = xdata.mean(axis=0)
            xdata_var = xdata.std(axis=0)**2
            train_var = w_1 * xdata_var + w_2 * train_var + w_3 * \
                    (xdata_mean - train_mean)**2
            train_mean = w_1 * xdata_mean + w_2 * train_mean
            ndpoints += xdata.shape[0]

        self.train_mean = train_mean
        self.train_std = (train_var**0.5).clip(min=1e-10)


    def validate_new_datapoints(self, input_x):
        """Checks new input data supplied by caller to
        ensure it is compatible with the dimensionality
        of the data used to fit the model.

        Args:
            input_x (np.ndarray): A numpy array containing
                raw input data.

        Returns:
            valid_data (bool): True if input was acceptable,
                False otherwise.
        """
        valid_data = True
        if len(input_x.shape) != len(self.xdim):
            valid_data = False
        if len(self.xdim) == 3:
            if input_x.shape[2] != self.xdim[2]:
                valid_data = False
        if input_x.shape[1] != self.xdim[1]:
            valid_data = False
        return valid_data



    def transform_x(self, input_x, multiply_by_beta = True, pretransformed = False):
        """Generates random Fourier features appropriate to the selected
        kernel for the input_x array. pretransform_x and finish_transform
        are implemented by child classes.

        Args:
            input_x: A numpy or cupy array.
            multiply_by_beta: If False, the random features are not multiplied
                by beta (the amplitude hyperparameter shared by all classes).
                Used for gridsearch optimization. Defaults to True.
            pretransformed (bool): If True, the random features have already
                been generated and a reference to input_x can be returned.
                Defaults to False.

        Returns:
            output_x: A numpy or cupy array depending on self.device containing
                the generated random features.
        """
        if pretransformed:
            return input_x.astype(self.out_type)
        else:
            output_x = self.pretransform_x(input_x)
            return self.finish_transform(output_x, multiply_by_beta)



    def get_hyperparams(self, logspace = True):
        """Returns the kernel hyperparameters. We have not used the property
        decorator since the logspace option is required.

        Args:
            logspace (bool): If True, the natural log of the hyperparameters is
                returned. Defaults to True.

        Returns:
            hyperparameters (np.ndarray): A numpy array of shape (N) for N
                kernel hyperparameters.
        """
        if logspace:
            return np.log(self.hyperparams)
        return self.hyperparams



    def set_hyperparams(self, hyperparams, logspace = True):
        """Sets the kernel hyperparameters. We have not used the property
        decorator since the logspace option is required.

        Args:
            hyperparams (np.ndarray): A numpy array of shape N for N hyperparameters.
                This function does not check for validity since it is often
                used by optimization algorithms that are merely modifying
                hyperparameters they retrieved from get_hyperparams. A caller
                that is passing values which may be invalid should call
                self.check_hyperparams first.
            logspace (bool): If True, the natural log of the hyperparameters is
                returned. Defaults to True.

        Returns:
            hyperparameters (np.ndarray): A numpy array of shape (N) for N
                kernel hyperparameters.
        """
        if logspace:
            self.hyperparams = np.exp(hyperparams)
        else:
            self.hyperparams = hyperparams


    def get_lambda(self):
        """For convenience, we enable caller to retrieve only the
        first hyperparameter, which is needed for a variety of
        operations during fitting and tuning. This hyperparameter
        determines the 'noise level' of the data."""
        return self.hyperparams[0]


    def check_hyperparams(self, hyperparams):
        """Checks a suggested set of hyperparameters passed
        by caller to ensure they are valid. This should be used
        when callers want to set the hyperparameters to user-specified
        values. The optimization algorithms bypass this because
        they are merely modifying hyperparameters retrieved from
        the kernel.

        Args:
            hyperparams (np.ndarray): A numpy array of shape (N), where
                N is the number of hyperparameters.

        Raises:
            ValueError: Raises a ValueError if invalid hyperparameters are
                passed.
        """
        if not isinstance(hyperparams, np.ndarray):
            raise ValueError("The starting hyperparameters must be a numpy array.")
        if hyperparams.shape != self.hyperparams.shape:
            raise ValueError(f"The kernel you selected uses {self.hyperparams.shape[0]} "
                "hyperparameters. A hyperparameter array of the incorrect shape was passed.")


    def nonshared_hparams_reg_grad(self, chol_zTz, weights,
                            dz_dsigma_ty, inner_deriv,
                            lambda_, hparams):
        """Calculates the gradient for kernel-specific hyperparameters,
        using inputs that are calculated by the appropriate function
        for each kernel to be kernel-specific. (The calculation
        can be broken down into kernel-specific and generic pieces --
        this is the generic piece). The gradient calculation here
        is for regression.

        Args:
            chol_zTz: A cupy or numpy array storing the cholesky decomposition
                of z^T z. Shape is (self.num_rffs, self.num_rffs).
            weights: A cupy or numpy array containing (z^T z + lambda)^-1 z^T y.
                Shape is (self.num_rffs).
            dz_dsigma_ty: A cupy or numpy array containing (dz_dsigma^T y).
                Shape is (self.num_rffs, M) where M is the number of kernel-
                specific hyperparameters.
            inner_deriv: A cupy or numpy array containing (dz_dsigma^T z +
                z^T dz_dsigma). Shape is (self.num_rffs, self.num_rffs, M)
                for M kernel-specific hyperparameters.
            lambda_ (float): The first hyperparameter (the noise value),
                which is shared between all kernels.
            hparams (np.ndarray): A numpy array containing the hyperparameters.
                This may have been modified by the kernel and may not match
                self.hyperparams.

        Returns:
            grad: A numpy array of shape (M) for M kernel-specific
                hyperparameters containing the gradient.
        """
        grad = np.zeros((dz_dsigma_ty.shape[1]))
        for i in range(grad.shape[0]):
            trace_term = self.cho_solver(chol_zTz, inner_deriv[:,:,i])
            dnll_dsigma = 2 * (weights.T @ dz_dsigma_ty[:,i])
            dnll_dsigma -= (weights.T @ (inner_deriv[:,:,i] @ weights))
            dnll_dsigma *= (-0.5 / lambda_**2)
            dnll_dsigma += 0.5 * trace_term.trace()
            grad[i] = float(dnll_dsigma)
        return grad * hparams[2:]



    def shared_hparams_reg_grad(self, z_trans_z, z_trans_y, y_trans_y,
                                    lambda_, beta_, ndatapoints):
        """Calculates the gradient for hyperparameters shared between
        all kernels, namely the first two: lambda_ (the noise) and beta_
        (the amplitude). The calculation here is the same for all kernels.
        The gradient calculation here is for regression.

        Args:
            z_trans_z: Numpy or cupy array of shape (self.num_rffs, self.num_rffs)
                containing z^T z.
            z_trans_y: Numpy or cupy array of shape (self.num_rffs) containing
                z^T y.
            y_trans_y (float): The dot product y^T y.
            lambda_ (float): The value of the first hyperparameter (noise) shared
                between all kernels. This may have been modified by an optimizer
                and may not match self.hyperparams.
            beta_ (float): The value of the second hyperparameter (amplitude)
                shared between all kernels. This may have been modified by
                an optimizer and may not match self.hyperparams.

        Returns:
            z_trans_z_chol: Numpy or cupy array containing the cholesky decomposition
                of (z_trans_z + lambda_ I).
            weights: Numpy or cupy array containing (z_trans_z + lambda_)^-1 z^T y.
            dnll_dlambda (float): The gradient of the NMLL w/r/t lambda_.
            dnll_dbeta (float): The gradient of the NMLL w/r/t beta_.
        """
        z_trans_z.flat[::z_trans_z.shape[0]+1] += lambda_**2
        if self.device == "gpu":
            weights, z_trans_z_chol, inner_deriv, chol_inv = gpu_cho_calcs(z_trans_z,
                    z_trans_y, lambda_)
        else:
            weights, z_trans_z_chol, inner_deriv, chol_inv = cpu_cho_calcs(z_trans_z,
                    z_trans_y, lambda_)

        #First calculate gradient w/r/t lambda...
        dnll_dlambda = (1 / lambda_**3) * ((z_trans_y.T @ weights) - y_trans_y)
        dnll_dlambda += (1 / lambda_) * (weights.T @ weights)
        dnll_dlambda += (ndatapoints - z_trans_z.shape[1]) / lambda_
        dnll_dlambda += lambda_ * (chol_inv**2).sum()
        dnll_dlambda = float(dnll_dlambda) * lambda_

        #All kernels have the beta hyperparameter -- calculate gradient w/r/t this...
        dnll_dbeta = (weights.T @ (z_trans_z.T @ weights)) - (z_trans_y.T @ weights)
        dnll_dbeta *= 1 / (lambda_**2 * beta_)
        dnll_dbeta += (1 / beta_) * inner_deriv.trace()
        dnll_dbeta = float(dnll_dbeta) * beta_

        return z_trans_z_chol, weights, dnll_dlambda, dnll_dbeta


    def get_num_rffs(self):
        """Returns number of RFFs. Not a @property because
        we do not want to define a setter, external classes
        should not be able to set."""
        return self.num_rffs


    @property
    def device(self):
        """Getter for the device property, which determines
        whether calculations are on CPU or GPU."""
        return self.device_


    @device.setter
    def device(self, value):
        """Setter for device, which determines whether calculations
        are on CPU or GPU. Note that each kernel must also have
        a kernel_specific_set_device function (enforced via
        an abstractmethod) to make any kernel-specific changes
        that occur when the device is switched.

        Args:
            value (str): Must be one of 'cpu', 'gpu'.

        Raises:
            ValueError: A ValueError is raised if an unrecognized
                device is passed.

        Note that a number of 'convenience attributes' (e.g. self.dtype,
        self.zero_arr) are set as references to either cupy or numpy functions.
        This avoids having to write two sets of functions (one for cupy, one for
        numpy) for each gradient calculation when the steps involved are the same.
        Also note that cupy uses float32, which is 5-10x faster on GPU; on CPU,
        float32 provides a much more modest benefit and float64 is used instead.
        """
        if value == "cpu":
            self.empty = np.empty
            self.zero_arr = np.zeros
            self.out_type = np.float64
            self.cho_solver = cpu_cho_solver
            if self.double_precision:
                self.dtype = np.float64
            else:
                self.dtype = np.float32

        elif value == "gpu":
            self.empty = cp.empty
            self.zero_arr = cp.zeros
            self.out_type = cp.float64
            self.cho_solver = gpu_cho_solver
            if self.double_precision:
                self.dtype = cp.float64
            else:
                self.dtype = cp.float32
        else:
            raise ValueError("Unrecognized device supplied. Must be one "
                    "of 'cpu', 'gpu'.")
        self.device_ = value
        self.kernel_specific_set_device(value)
