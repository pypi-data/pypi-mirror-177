"""A randomized Nystrom preconditioner for conjugate gradients.
For CUDA only."""
from math import ceil

try:
    import cupy as cp
    import cupyx
    from cupyx.scipy import linalg
except:
    pass
import numpy as np
from ..kernels.srht_compressor import SRHTCompressor



class CudaRandomizedPreconditioner():
    """Implements a preconditioner based on the randomized
    Nystrom approximation to the inverse of Z^T Z + lambda.)

    Attributes:
        lambda_ (float): The noise hyperparameter shared by all kernels.
        verbose (bool): If True, print regular updates.
        min_target (float): If performing adaptive rank selection,
            this value is our 'goal' for an acceptable lambda / min_eigval
            ratio.
        achieved_ratio (float): lambda_ / min_eig, where min_eig is the
            smallest eigenvalue for the preconditioner. This is a
            reasonably good predictor of how effective the preconditioner
            will be. Smaller is better.
        prefactor (float): A constant by which the matvec is multiplied
            when performing matvecs with the preconditioner.
        u_mat (cp.ndarray): A cupy array containing the eigenvectors of
            the matrix formed during preconditioner construction. Used
            together with prefactor and inv_eig to perform the matvec
            that approximates A^-1.
        inv_eig (cp.ndarray): A cupy array containing the inverse of the
            eigenvalues of the matrix formed during preconditioner construction.
        eig (cp.ndarray): A cupy array containing the
            eigenvalues of the matrix formed during preconditioner construction.
        min_eig (float): The minimum eigval from preconditioner construction.
    """

    def __init__(self, lambda_, verbose):
        """Class constructor.

        Args:
            lambda_ (float): The noise hyperparameter shared by all kernels.
            verbose (bool): If True, print regular updates.
        """
        self.lambda_ = lambda_
        self.verbose = verbose
        self.min_target = 10
        self.achieved_ratio = None
        self.prefactor = None
        self.u_mat = None
        self.inv_eig = None
        self.eig = None
        self.min_eig = None


    def prep_operator(self, kernel, dataset, fitting_rffs,
                            max_rank, random_state = 123,
                            method = "srht"):
        """Constructs the matrices necessary to use the preconditioner.
        Args:
            kernel: A valid kernel object that can generate random features.
            dataset: An OnlineDataset or OfflineDataset that contains the raw
                data.
            fitting_rffs (int): The number of random features expected.
            max_rank (int): The max rank accepted for the preconditioner.
            random_state (int): Seed for the random number generator.
            method (str): one of "srht" or "gauss". srht is MUCH faster for
                large datasets. gauss is faster for small datasets.

        Returns:
            failure (bool): If False, the preconditioner was constructed
                successfully. If True, it should not be used.
        """
        if self.verbose:
            print("Now building preconditioner.")
        failure = False
        if method == "srht":
            self.u_mat, self.inv_eig, self.min_eig = self.get_srht_nystrom_decomp(dataset,
                           max_rank, fitting_rffs,
                           kernel, random_state)
        else:
            self.u_mat, self.inv_eig, self.min_eig = self.get_nystrom_decomp(dataset,
                           max_rank, fitting_rffs,
                           kernel, random_state)

        if self.u_mat is None:
            failure = True
            return failure
        self.achieved_ratio = self.min_eig / self.lambda_**2
        self.prefactor = float(self.min_eig + self.lambda_**2)

        if self.verbose:
            print(f"Min eigval / lambda**2: {self.achieved_ratio}")
        return failure


    def matvec(self, x):
        """Returns a matvec of the preconditioner with an input
        vector x."""
        xprod = self.u_mat.T @ x
        xprod1 = self.u_mat @ (self.inv_eig * self.prefactor * xprod)
        xprod2 = x - (self.u_mat @ xprod)
        return xprod2 + xprod1


    def batch_matvec(self, x):
        """Multiplies the preconditioner against batched input.
        TODO: Vectorize this, as written it is not efficient.
        (Fortunately this is not frequently used)."""
        x_out = cp.empty((x.shape[0], x.shape[1]))
        for i in range(x_out.shape[1]):
            xprod = self.u_mat.T @ x[:,i]
            xprod1 = self.u_mat @ (self.inv_eig * self.prefactor * xprod)
            xprod2 = x[:,i] - (self.u_mat @ xprod)
            x_out[:,i] = xprod2 + xprod1
        return x_out


    def fwd_matvec(self, x):
        """Returns a matvec of the preconditioner inverse (an approximation
        of the original matrix) with an input vector x."""
        xprod = self.u_mat.T @ x
        xprod1 = self.u_mat @ (self.eig * xprod)
        xprod2 = x - (self.u_mat @ xprod)
        return xprod2 + xprod1 / self.prefactor


    def get_rank(self):
        """Returns the preconditioner rank."""
        return self.inv_eig.shape[0]


    def get_min_eig(self):
        """Returns the min eigval."""
        return self.min_eig


    def get_nystrom_decomp(self, dataset, rank, fitting_rffs,
                                    kernel, random_state):
        """Builds the randomized Nystrom approximation to the inverse
        of (z^T z + lambda), where z is the random features generated
        for dataset.

        Args:
            dataset: An OnlineDataset or OfflineDataset containing the raw data.
            rank (int): The desired rank of the preconditioner.
            fitting_rffs (int): The number of expected random features.
            kernel: A valid kernel object that can generate random features.
            random_state (int): A seed for the random number generator.

        Returns:
            u_mat (cp.ndarray): The eigenvectors of the matrix needed to
                form the preconditioner.
            s_inv (cp.ndarray): The inverse of the eigenvalues of the
                matrix needed to form the preconditioner.
            min_eig (cp.ndarray): The minimum eigenvalue for the preconditioner,
                can be used to assess how useful preconditioner will be.
        """
        mempool = cp.get_default_memory_pool()
        mempool.free_all_blocks()

        rng = cp.random.default_rng(random_state)
        np_rng = np.random.default_rng(random_state)
        l_mat = rng.standard_normal(size=(fitting_rffs, rank), dtype=cp.float64)
        l_mat, _ = cp.linalg.qr(l_mat)
        acc_results = cp.zeros((fitting_rffs, rank))

        j = 0
        for xdata in dataset.get_chunked_x_data():
            xtrans = kernel.transform_x(xdata,
                pretransformed = dataset.pretransformed)
            acc_results += xtrans.T @ (xtrans @ l_mat)
            if j % 10 == 0 and self.verbose:
                print(f"Chunk {j} complete.")
            j += 1
        if self.verbose:
            print("Now compiling preconditioner results...")
        del xtrans
        norm = float(cp.sqrt((acc_results**2).sum())  )
        shift = np.spacing(norm)

        mempool.free_all_blocks()
        _ = cupyx.seterr(linalg="raise")
        acc_results += shift * l_mat

        #If the matrix is not positive definite, abort.
        #Very unlikely and unusual error.
        try:
            l_mat = l_mat.T @ acc_results
            c_mat = cp.linalg.cholesky(l_mat)
        except:
            self.achieved_ratio = 0
            return None, None, None
        del l_mat
        mempool.free_all_blocks()

        acc_results = cupyx.scipy.linalg.solve_triangular(c_mat, acc_results.T,
                            overwrite_b = True, lower=True).T
        u_mat, s_mat, _ = cp.linalg.svd(acc_results,
                            full_matrices=False)
        s_mat = (s_mat**2 - shift).clip(min=0.0)
        min_eig = s_mat.min()

        s_inv = s_mat + self.lambda_**2
        self.eig = s_inv.copy()
        mask = s_inv > 1e-14
        s_inv[mask] = 1 / s_inv[mask]
        s_inv[mask==False] = 0.0
        return u_mat, s_inv, min_eig




    def get_srht_nystrom_decomp(self, dataset, rank, fitting_rffs,
                                    kernel, random_state):
        """Builds the randomized Nystrom approximation to the inverse
        of (z^T z + lambda), where z is the random features generated
        for dataset, using the SRHT.

        Args:
            dataset: An OnlineDataset or OfflineDataset containing the raw data.
            rank (int): The desired rank of the preconditioner.
            fitting_rffs (int): The number of expected random features.
            kernel: A valid kernel object that can generate random features.
            random_state (int): A seed for the random number generator.

        Returns:
            u_mat (cp.ndarray): The eigenvectors of the matrix needed to
                form the preconditioner.
            s_inv (cp.ndarray): The inverse of the eigenvalues of the
                matrix needed to form the preconditioner.
            min_eig (cp.ndarray): The minimum eigenvalue for the preconditioner,
                can be used to assess how useful preconditioner will be.
        """
        mempool = cp.get_default_memory_pool()
        np_rng = np.random.default_rng(random_state)
        acc_results = cp.zeros((rank, fitting_rffs))
        compressor = SRHTCompressor(rank, fitting_rffs, random_seed = random_state,
                device="gpu")

        j = 0
        #Unfortunately we have to use doubles here, this is one area where
        #loss of precision can lead to poor results.
        for xdata in dataset.get_chunked_x_data():
            xtrans = kernel.transform_x(xdata,
                pretransformed = dataset.pretransformed)
            xalt = compressor.transform_x(xtrans)
            acc_results += xalt.T @ xtrans
            if j % 10 == 0 and self.verbose:
                print(f"Chunk {j} complete.")
            j += 1
            mempool.free_all_blocks()

        if self.verbose:
            print("Now compiling preconditioner results...")
        del xtrans

        mempool.free_all_blocks()

        c_mat = compressor.transform_x(acc_results)
        _, c_s1, c_v1 = cp.linalg.svd(c_mat, full_matrices = False)
        mask = c_s1 < 1e-14
        c_s1 = 1 / cp.sqrt(c_s1.clip(min=1e-14))
        c_s1[mask] = 0
        acc_results = acc_results.T @ c_v1.T @ (c_s1[:,None] * c_v1)

        mempool.free_all_blocks()

        u_mat, s_mat, _ = cp.linalg.svd(acc_results,
                            full_matrices=False)
        s_mat = (s_mat**2).clip(min=0.0)
        min_eig = s_mat.min()

        s_inv = s_mat + self.lambda_**2
        self.eig = s_inv.copy()
        mask = s_inv > 1e-14
        s_inv[mask] = 1 / s_inv[mask]
        s_inv[mask==False] = 0.0
        return u_mat, s_inv, min_eig
