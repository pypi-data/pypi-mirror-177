"""A conjugate gradients implementation for cuda. Preferred to
cupy's since it offers us the ability to easily have
multiple outputs if needed. Implemented in Cython since
looping over a numpy array is slow in pure Python."""
import numpy as np
cimport numpy as np
try:
    import cupy as cp
except:
    pass


cdef class GPU_ConjugateGrad:
    """Performs conjugate gradients to find b in Ab = y.

    Attributes:
        lambda_ (double): The noise hyperparameter shared
            by all kernels.
        fitting_rffs (int): The number of random features
            expected.
    """
    cdef double lambda_
    cdef int fitting_rffs

    def __init__(self, double lambda_, int fitting_rffs):
        """Class constructor.

        Args:
            lambda_ (double): The noise hyperparameter shared
                by all kernels.
            fitting_rffs (int): The number of random features
                expected.
        """
        self.lambda_ = lambda_
        self.fitting_rffs = fitting_rffs


    def _matvec(self, dataset, kernel, vec):
        """Performs a matvec operation (Z^T Z + lambda) vec,
        where Z is the random features for the raw data
        from dataset.

        Args:
            dataset: An OnlineDataset or OfflineDataset object
                with the raw data.
            kernel: A valid kernel object.
            vec (cp.ndarray): The product Z^T y.
        
        Returns:
            matvec (cp.ndarray): The product (Z^T Z + lambda) vec.
        """
        matvec = cp.zeros(vec.shape)
        for x in dataset.get_chunked_x_data():
            Z = kernel.transform_x(x, pretransformed =
                dataset.pretransformed)
            matvec += Z.T @ (Z @ vec)
        matvec += self.lambda_**2 * vec
        return matvec


    def get_zTy(self, dataset, kernel):
        """Performs a matvec operation Z^T y,
        where Z is the random features for the raw data
        from dataset.

        Args:
            dataset: An OnlineDataset or OfflineDataset object
                with the raw data.
            kernel: A valid kernel object.
        
        Returns:
            zTy (cp.ndarray): The product Z^T y.
        """
        zTy = cp.zeros(self.fitting_rffs)
        for x, y in dataset.get_chunked_data():
            Z = kernel.transform_x(x, pretransformed =
                dataset.pretransformed)
            zTy += Z.T @ y.astype(cp.float64)
        return zTy


    def fit(self, dataset, kernel, preconditioner, 
            zTy, int maxiter = 200,
            double tol = 1e-4, 
            bint verbose = True):
        """Performs conjugate gradients to evaluate (Z^T Z + lambda)^-1 Z^T y,
        where Z is the random features generated for the dataset and lambda
        is the shared noise hyperparameter.

        Args:
            dataset: An OnlineDataset or OfflineDataset with the raw data.
            kernel: A valid kernel object.
            preconditioner: Either None or a valid preconditioner object.
            zTy (cp.ndarray): The product Z^T y.
            maxiter (int): The maximum number of iterations.
            tol (double): The threshold for convergence.
            verbose (bint): If True, print regular updates.
        
        Returns:
            xk (cp.ndarray): The result of (Z^T Z + lambda)^-1 Z^T y.
            converged (bint): If False, we did not converge, just ran
                into maxiter.
            niter: The number of iterations.
        """
        cdef int niter
        cdef int next_col, current_col
        cdef double err
        cdef bint converged
        losses = []
        niter = 0

        dtype = cp.float64
        zk = cp.zeros((zTy.shape[0], 2), dtype=dtype)
        pk = cp.zeros((zTy.shape[0], 2), dtype=dtype)
        alpha = cp.zeros((2), dtype=dtype)
        beta = cp.zeros((2), dtype=dtype)

        resid = cp.zeros((zTy.shape[0], 2), dtype=dtype)
        xk = cp.zeros(zTy.shape[0], dtype=dtype)

        bnorm = cp.linalg.norm(zTy)
        resid[:,0] = zTy / bnorm
        if preconditioner is None:
            zk[:,0] = resid[:,0]
        else:
            zk[:,0] = preconditioner.matvec(resid[:,0])
        pk[:,0] = zk[:,0]

        converged = False

        next_col, current_col = 1, 0
        for niter in range(maxiter - 1):
            w = self._matvec(dataset, kernel, pk[:,current_col])
            alpha[next_col] = (resid[:,current_col] * 
                    zk[:,current_col]).sum(axis=0) / \
                    (pk[:,current_col] * w).sum(axis=0)
            xk += alpha[None,next_col] * pk[:,current_col]
            resid[:,next_col] = resid[:,current_col] - \
                                alpha[None,next_col] * w
            
            if preconditioner is None:
                zk[:,next_col] = resid[:,next_col]
            else:
                zk[:,next_col] = preconditioner.matvec(resid[:,next_col])
            beta[next_col] = (resid[:,next_col] * zk[:,next_col]).sum(axis=0) / \
                                (resid[:,current_col] * 
                                zk[:,current_col]).sum(axis=0)
            pk[:,next_col] = zk[:,next_col] + beta[None,next_col] * \
                                    pk[:,current_col]

            err = cp.linalg.norm(resid[:,current_col], axis=0)
            next_col = abs(next_col - 1)
            current_col = abs(current_col - 1)
            
            if niter % 5 == 0 and verbose:
                print("%s iterations complete."%niter)

            niter += 1
            losses.append(err)
            if err < tol:
                converged = True
                break

        return xk * bnorm, converged, niter, losses
