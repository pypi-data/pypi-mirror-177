"""The radial basis function -- the most generic and popular of all
kernels."""
import numpy as np
from ..sorf_kernel_baseclass import SORFKernelBaseclass


class RBF(SORFKernelBaseclass):
    """The RBF is the classic kernel and a perennial favorite. A GP
    equipped with this functions as a high-dimensional smoother.
    This class inherits from SORFKernelBaseclass which in turn inherits
    from KernelBaseclass. Only attributes unique to this child are
    described in this docstring.

    Attributes:
        hyperparams (np.ndarray): A length three array of three
            hyperparameters: lambda_ (noise), beta_ (amplitude)
            and sigma (inverse lengthscale).
        cosfunc: A convenience reference to either cp.cos or np.cos,
            as appropriate for current device.
        sinfunc: A convenience reference to either cp.sin or np.sin,
            as appropriate for current device.
    """

    def __init__(self, xdim, num_rffs, random_seed = 123,
                device = "cpu", double_precision = True, **kwargs):
        """Constructor for RBF.

        Args:
            xdim (tuple): The dimensions of the input.
            num_rffs (int): The user-requested number of random Fourier features.
            random_seed (int): The seed to the random number generator.
            device (str): One of 'cpu', 'gpu'. Indicates the starting device.
            double_precision (bool): If True, generate random features in double precision.
                Otherwise, generate as single precision.
            **kwargs: Some kernels require additional arguments. To preserve
                a common interface, this kernel accepts and ignores these
                **kwargs.
        """
        super().__init__(num_rffs, xdim, double_precision,
                sine_cosine_kernel = True, random_seed = random_seed)
        self.hyperparams = np.ones((3))
        bounds = np.asarray([[1e-3,1e1], [0.2, 5], [1e-6, 1e2]])
        self.set_bounds(bounds, logspace=False)

        self.device = device
