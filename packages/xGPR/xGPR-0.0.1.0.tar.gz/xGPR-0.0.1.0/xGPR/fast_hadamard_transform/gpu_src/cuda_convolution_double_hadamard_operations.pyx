"""Handles hadamard transform-based convolution operations for sequences and graphs
if the input array is an array of doubles."""
#cython: language_level=3
import numpy as np
cimport numpy as np
cimport cython
from libc cimport stdint
import cupy as cp
from libc.stdint cimport uintptr_t
import math
from libc.stdint cimport int8_t


cdef extern from "convolution.h" nogil:
    const char *doubleConv1dPrep_(int8_t *radem,
                double *reshapedx, int reshapeddim0, 
                int reshapeddim1, int reshapeddim2,
                int startposition, int numfreqs)

cdef extern from "poly_fht.h":
    const char *doublePolyFHTPrep_(int8_t *radem, double *reshapedX, int reshapedDim0,
                int reshapedDim1, int reshapedDim2, int numFreqs,
                int columnStartPosition, int rowStartPosition)



@cython.boundscheck(False)
@cython.wraparound(False)
def doubleGpuConv1dTransform(reshapedX, radem, Z, S, int numThreads, double sigma, 
                str mode):
    """Uses the wrapped doubleConv1dPrep_ and cupy operations to perform a
    structured orthogonal random features or SORF operation on
    an array of doubles that has been reshaped to perform convolution.
    Note that doubleConv1dPrep should ONLY be accessed through this
    since this wrapper performs key checks (the shape of the input
    arrays, are they C-contiguous etc.) that should not be bypassed.

    Args:
        reshapedX (cp.ndarray): An array of type float64 from which
            the features will be generated. Is not modified. Must
            be of shape (N x D x C) where C is a power of 2. Should
            have been reshaped to be appropriate for convolution.
        radem (cp.ndarray): A stack of diagonal matrices of type int8_t
            of shape (3 x 1 x m * C), where R is the number of random
            features requested and m is ceil(R / C).
        Z (cp.ndarray): An N x R array in which the output features
            will be stored.
        S (cp.ndarray): A stack of diagonal matrices stored as an
            array of shape (R) drawn from a chi distribution.
        num_threads (int): This argument is so that this function has
            the same interface as the CPU SORF Transform. It is not
            needed for the GPU transform and is ignored.
        sigma (double): The kernel specific hyperparameter for the
            Conv1d kernel.
        mode (str): One of 'maxpool', 'maxpool_loc', 'conv', 'conv_gradient'.
            Determines the type of activation function and pooling that
            is performed.

    Returns:
        gradient (cp.ndarray): A float64 array of shape (N x R) if
            mode is "conv_gradient"; otherwise nothing.
    """
    cdef const char *errCode
    cdef int i, startPosition, cutoff
    cdef double scalingTerm
    cdef int num_repeats = (radem.shape[2] + reshapedX.shape[2] - 1) / reshapedX.shape[2]
    reshapedXCopy = reshapedX.copy()
    
    if mode not in ["maxpool", "maxpool_loc", "conv", "conv_gradient"]:
        raise ValueError("Invalid mode supplied for convolution.")

    #Check that all arrays have expected sizes and data types.    
    if reshapedX.shape[0] == 0:
        raise ValueError("There must be at least one datapoint.")
    if reshapedX.shape[0] != Z.shape[0]:
        raise ValueError("The number of input and output datapoints do not "
                "agree.")
    if not len(radem.shape) == 3:
        raise ValueError("radem must be a 3d array.")
    if not len(S.shape) == 1 or not len(Z.shape) == 2:
        raise ValueError("S must be a 1d array; Z must be 2d.")
    if not len(reshapedX.shape) == 3:
        raise ValueError("X must be a 3d array.")
    if not radem.dtype == "int8":
        raise ValueError("radem must be int8.")
    if not Z.dtype == "float64" or not reshapedX.dtype == "float64":
        raise ValueError("reshapedX, Z must be float64.")
    if not S.dtype == "float64":
        raise ValueError("S must be float64.")


    #Check that shapes of radem, Z are correct.
    if radem.shape[0] != 3 or radem.shape[1] != 1:
        raise ValueError("radem must have length 3 for dim 0 and length 1 for dim1.")
    if mode.startswith("maxpool"):
        if Z.shape[1] != radem.shape[2]:
            raise ValueError("Z.shape[1] must be an integer multiple of the next largest "
                "power of 2 greater than the kernel width * X.shape[2].")
    elif Z.shape[1] != 2 * radem.shape[2]:
        raise ValueError("Z.shape[1] must be 2 * radem.shape[2], which must be an integer "
                "multiple of the next largest power of 2 greater than the kernel width * "
                "X.shape[2].")

    #Next, make sure that reshapedX and S make sense.
    if S.shape[0] != radem.shape[2]:
        raise ValueError("S.shape[0] must == radem.shape[2].")
        
    logdim = np.log2(reshapedX.shape[2])
    if np.ceil(logdim) != np.floor(logdim) or reshapedX.shape[2] < 2:
        raise ValueError("dim2 of the reshapedX array must be a power of 2 >= 2.")
    if not radem.shape[2] % reshapedX.shape[2] == 0:
        raise ValueError("The number of sampled frequencies should be an integer multiple of "
                "reshapedX.shape[2].")

    #Make sure that all inputs are C-contiguous.
    if not Z.flags["C_CONTIGUOUS"] or not reshapedX.flags["C_CONTIGUOUS"] \
            or not radem.flags["C_CONTIGUOUS"] or not S.flags["C_CONTIGUOUS"]:
        raise ValueError("One or more arguments is not C contiguous.")


    cdef uintptr_t addr_reshapedCopy = reshapedXCopy.data.ptr
    cdef double *reshapedXCopyPtr = <double*>addr_reshapedCopy
    
    cdef uintptr_t addr_radem = radem.data.ptr
    cdef int8_t *radem_ptr = <int8_t*>addr_radem
    
    startPosition, cutoff = 0, reshapedX.shape[2]
    scalingTerm = np.sqrt(1 / <double>radem.shape[2])
    if mode == "conv_gradient":
        gradient = cp.zeros((Z.shape[0], Z.shape[1]), dtype=cp.float64)
    
    for i in range(num_repeats):
        reshapedXCopy[:] = reshapedX
        errCode = doubleConv1dPrep_(radem_ptr,
                    reshapedXCopyPtr, reshapedX.shape[0], reshapedX.shape[1], 
                    reshapedX.shape[2], i * reshapedX.shape[2],
                    radem.shape[2])
        if errCode.decode("UTF-8") != "no_error":
            raise Exception("Fatal error encountered in doubleGpuConv1dTransform_.")
        
        reshapedXCopy *= S[None,None,(i * reshapedX.shape[2]):((i+1) * reshapedX.shape[2])]
        if mode == "maxpool":
            Z[:,startPosition:cutoff] = reshapedXCopy.max(axis=1)
        elif mode == "maxpool_loc":
            Z[:,startPosition:cutoff] = reshapedXCopy.max(axis=1)
            Z[:,startPosition:cutoff] -= reshapedXCopy.mean(axis=1)
        elif mode == "conv_gradient":
            featureMod = sigma * reshapedXCopy

            Z[:,startPosition:cutoff] = cp.cos(featureMod).sum(axis=1)
            gradient[:,startPosition:cutoff] = (-cp.sin(featureMod) * \
                                reshapedXCopy).sum(axis=1)
            cutoff += reshapedX.shape[2]
            startPosition += reshapedX.shape[2]
            Z[:,startPosition:cutoff] = cp.sin(featureMod).sum(axis=1)
            gradient[:,startPosition:cutoff] = (cp.cos(featureMod) * \
                                reshapedXCopy).sum(axis=1)
        elif mode == "conv":
            reshapedXCopy *= sigma
            Z[:,startPosition:cutoff] = cp.sum(cp.cos(reshapedXCopy), axis=1)
            cutoff += reshapedX.shape[2]
            startPosition += reshapedX.shape[2]
            Z[:,startPosition:cutoff] = cp.sum(cp.sin(reshapedXCopy), axis=1)

        cutoff += reshapedX.shape[2]
        startPosition += reshapedX.shape[2]
    
    if not mode.startswith("maxpool"):
        Z *= scalingTerm
    if mode == "conv_gradient":
        gradient *= scalingTerm
        return gradient



@cython.boundscheck(False)
@cython.wraparound(False)
def doubleGpuGraphConv1dTransform(reshapedX, radem, Z, S,
                int numThreads,
                np.ndarray[np.float64_t, ndim=1] sigmaValues,
                np.ndarray[np.int64_t, ndim=1] splitPoints,
                str mode = "standard"):
    """Uses the wrapped doubleConv1dPrep_ and numpy operations to perform
    1d convolution on a sequence of vectors representing the nodes
    of a graph, using an array of doubles. Has the capability to use
    different lengthscales for different 'segments' of each node
    vector (up to 3).

    Args:
        reshapedX (cp.ndarray): Raw data reshaped so that a convolution can be
            performed on it using orthogonal random features with the SORF
            operation. This array is not modified in place -- rather the features
            that are generated are stored in Z. Shape is (N x D x C) for 
            N datapoints. C must be a power of 2.
        radem (cp.ndarray): A stack of diagonal matrices with elements drawn from the
            Rademacher distribution. Shape must be (3 x D x C).
        Z (cp.ndarray): A numpy array in which the generated features will be
            stored. Is modified in-place.
        S (cp.ndarray): A stack of diagonal matrices stored as an
            array of shape m * C drawn from a chi distribution.
        num_threads (int): Number of threads to use for FHT.
        sigmaValues (np.ndarray): The lengthscale for each section of the input.
            shape[0] must == splitPoints.shape[0] - 1.
        splitPoints (np.ndarray): The points at which to split the input when
            applying different lengthscales. splitPoints.shape[0] == sigmaValues.shape[0] + 1.
        mode (str): Either 'standard' or 'gradient'. If 'gradient' a gradient array is returned.

    Raises:
        ValueError: A ValueError is raised if unexpected or invalid inputs are supplied.

    Returns:
        gradient (cp.ndarray); An array of shape output.shape[0] x output.shape[1] x sigmaValues.shape[0].
            Only returned if mode == "gradient"; otherwise, nothing is returned.
    """
    cdef const char *errCode
    reshapedXCopy = reshapedX.copy()
    cdef double scalingTerm
    cdef int num_repeats = (radem.shape[2] + reshapedX.shape[2] - 1) / reshapedX.shape[2]
    cdef int startPosition, cutoff, startPos2, cutoff2, i, j

    if mode not in ["standard", "gradient"]:
        raise ValueError("Invalid mode supplied for convolution.")

    if splitPoints.shape[0] != sigmaValues.shape[0] + 1:
        raise ValueError("The splitPoints supplied to graph convolution should have "
                "shape[0] == hyperparams[2:] + 1.")

    if len(S.shape) != 1 or len(radem.shape) != 3 or len(reshapedX.shape) != 3:
        raise ValueError("S should be a 1d array. radem and reshapedX should be 3d arrays.")
    if len(Z.shape) != 2:
        raise ValueError("Z should be a 2d array.")

    if reshapedX.shape[0] == 0:
        raise ValueError("There must be at least one datapoint.")
    if reshapedX.shape[0] != Z.shape[0]:
        raise ValueError("The number of datapoints in the outputs and the inputs do "
                "not agree.")
    if radem.shape[0] != 3 or radem.shape[1] != 1:
        raise ValueError("radem must have length 3 for dim 0 and length 1 for dim1.")
    if Z.shape[1] != 2 * radem.shape[2]:
        raise ValueError("Z.shape[1] must be 2 * radem.shape[2], which must be an integer multiple of "
                    "the next power of 2 greater than the kernel width * X.shape[2].")
    
    if S.shape[0] != radem.shape[2]:
        raise ValueError("S.shape[0] must == radem.shape[2].")
    logdim = np.log2(reshapedX.shape[2])
    if np.ceil(logdim) != np.floor(logdim) or reshapedX.shape[2] < 2:
        raise ValueError("dim2 of the reshapedX array must be a power of 2 >= 2.")
    if not radem.shape[2] % reshapedX.shape[2] == 0:
        raise ValueError("The number of sampled frequencies should be an integer multiple of "
                "reshapedX.shape[2].")
    
    if not radem.dtype == "int8":
        raise ValueError("radem must be int8.")
    if not Z.dtype == "float64" or not reshapedX.dtype == "float64":
        raise ValueError("reshapedX, Z must be float64.")
    if not S.dtype == "float64":
        raise ValueError("S must be float64.")

    if not Z.flags["C_CONTIGUOUS"] or not reshapedX.flags["C_CONTIGUOUS"] or not radem.flags["C_CONTIGUOUS"] \
        or not S.flags["C_CONTIGUOUS"]:
        raise ValueError("One or more arguments is not C contiguous.")

    featureMod = cp.zeros((reshapedX.shape[0], reshapedX.shape[1], reshapedX.shape[2]),
                            dtype = cp.float64)

    cdef uintptr_t addr_reshapedCopy = reshapedXCopy.data.ptr
    cdef double *reshapedXCopyPtr = <double*>addr_reshapedCopy
    cdef uintptr_t addr_featureMod = featureMod.data.ptr
    cdef double *featureModPtr = <double*>addr_featureMod
 
    cdef uintptr_t addr_radem = radem.data.ptr
    cdef int8_t *radem_ptr = <int8_t*>addr_radem


    startPosition, cutoff = 0, reshapedX.shape[2]
    startPos2, cutoff2 = reshapedX.shape[2], cutoff + reshapedX.shape[2]
    scalingTerm = np.sqrt(1 / <double>radem.shape[2])
    if mode == "gradient":
        gradient = cp.zeros((Z.shape[0], Z.shape[1], sigmaValues.shape[0]), dtype=cp.float64)

    for i in range(num_repeats):
        reshapedXCopy[:] = reshapedX
        for j in range(0, splitPoints.shape[0] - 1):
            reshapedXCopy[:,:,splitPoints[j]:splitPoints[j+1]] *= sigmaValues[j]
        errCode = doubleConv1dPrep_(radem_ptr,
                    reshapedXCopyPtr, reshapedX.shape[0], reshapedX.shape[1], 
                    reshapedX.shape[2], i * reshapedX.shape[2],
                    radem.shape[2])
        if errCode.decode("UTF-8") != "no_error":
            raise Exception("Fatal error encountered while performing graph convolution.")
        reshapedXCopy *= S[None,None,(i * reshapedX.shape[2]):((i+1) * reshapedX.shape[2])]
        if mode == "gradient":
            if splitPoints.shape[0] == 2:
                gradient[:,startPosition:cutoff,0] = (-cp.sin(reshapedXCopy) * reshapedXCopy /
                                            sigmaValues[0]).sum(axis=1)
                gradient[:,startPos2:cutoff2,0] = (cp.cos(reshapedXCopy) * reshapedXCopy /
                                        sigmaValues[0]).sum(axis=1)
            else:
                for j in range(0, splitPoints.shape[0] - 1):
                    featureMod[:] = 0
                    featureMod[:,:,splitPoints[j]:splitPoints[j+1]] = \
                        reshapedX[:,:,splitPoints[j]:splitPoints[j+1]]
                    errCode = doubleConv1dPrep_(radem_ptr,
                        featureModPtr, reshapedX.shape[0], reshapedX.shape[1], 
                        reshapedX.shape[2], i * reshapedX.shape[2],
                        radem.shape[2])
                    if errCode.decode("UTF-8") != "no_error":
                        raise Exception("Fatal error encountered while performing graph convolution.")
                    featureMod *= S[None,None,(i * reshapedX.shape[2]):((i+1) * reshapedX.shape[2])]
                    gradient[:,startPosition:cutoff,j] = (-cp.sin(reshapedXCopy) * featureMod).sum(axis=1)
                    gradient[:,startPos2:cutoff2,j] = (cp.cos(reshapedXCopy) * featureMod).sum(axis=1)

        Z[:,startPosition:cutoff] = cp.sum(cp.cos(reshapedXCopy), axis=1)
        Z[:,startPos2:cutoff2] = cp.sum(cp.sin(reshapedXCopy), axis=1)
        cutoff += 2 * reshapedX.shape[2]
        startPosition += 2 * reshapedX.shape[2]
        startPos2 += 2 * reshapedX.shape[2]
        cutoff2 += 2 * reshapedX.shape[2]

    Z *= scalingTerm
    if mode == "gradient":
        gradient *= scalingTerm
        return gradient


@cython.boundscheck(False)
@cython.wraparound(False)
def doubleGpuGraphPolyFHT(reshapedX, radem, S, Z, int polydegree,
                int numThreads):
    """Uses the wrapped PolyFHT_ and numpy operations to apply a pairwise
    polynomial kernel for graphs to float64 arrays.

    Args:
        reshapedX (cp.ndarray): Raw data reshaped so that the random features
            transformation can be applied. This array is not modified in place --
            rather the features that are generated are stored in Z. Shape is (N x D x C)
            for N datapoints. C must be a power of 2.
        radem (cp.ndarray): A stack of diagonal matrices with elements drawn from the
            Rademacher distribution. Shape must be (3 * polydegree x D x C).
        S (cp.ndarray): A stack of diagonal matrices stored as an
            array of shape polydegree x m * C drawn from a chi distribution.
        Z (cp.ndarray): An array in which the generated features will be
            stored. Is modified in-place.
        polydegree (int): The degree of the polynomial kernel that we approximate. Should
            be <= 4 (for very high-degree polynomial kernels we are probably better off
            switching to an RBF or convolution kernel).
        num_threads (int): Number of threads to use for FHT. Not used for gpu,
            merely kept here for consistency with CPU version.

    Raises:
        ValueError: A ValueError is raised if unexpected or invalid inputs are supplied.
    """
    cdef const char *errCode
    reshapedXCopy = reshapedX.copy()
    preSumFeats = reshapedX.copy()
    cdef double scalingTerm
    cdef int num_repeats = (radem.shape[2] + reshapedX.shape[2] - 1) / reshapedX.shape[2]
    cdef int startPosition, cutoff, i, j

    if len(S.shape) != 2 or len(radem.shape) != 3 or len(reshapedX.shape) != 3:
        raise ValueError("S should be a 2d array. radem and reshapedX should be 3d arrays.")
    if len(Z.shape) != 2:
        raise ValueError("Z should be a 2d array.")

    if reshapedX.shape[0] == 0:
        raise ValueError("There must be at least one datapoint.")
    if reshapedX.shape[0] != Z.shape[0]:
        raise ValueError("The number of datapoints in the outputs and the inputs do "
                "not agree.")
    if radem.shape[0] != 3 * polydegree or radem.shape[1] != 1:
        raise ValueError("radem must have length 3 * polydegree for dim 0 and length 1 for dim1.")
    if Z.shape[1] != radem.shape[2]:
        raise ValueError("Z.shape[1] must be radem.shape[2], which must be an integer multiple of "
                    "the next power of 2 greater than the kernel width * X.shape[2].")
    
    if S.shape[1] != radem.shape[2]:
        raise ValueError("S.shape[1] must == radem.shape[2].")
    if S.shape[0] != polydegree:
        raise ValueError("S.shape[0] must == polydegree.")
    logdim = np.log2(reshapedX.shape[2])
    if np.ceil(logdim) != np.floor(logdim) or reshapedX.shape[2] < 2:
        raise ValueError("dim2 of the reshapedX array must be a power of 2 >= 2.")
    if not radem.shape[2] % reshapedX.shape[2] == 0:
        raise ValueError("The number of sampled frequencies should be an integer multiple of "
                "reshapedX.shape[2].")

    if not Z.flags["C_CONTIGUOUS"] or not reshapedX.flags["C_CONTIGUOUS"] or not radem.flags["C_CONTIGUOUS"] \
        or not S.flags["C_CONTIGUOUS"]:
        raise ValueError("One or more arguments is not C contiguous.")
    
    if not radem.dtype == "int8":
        raise ValueError("radem must be int8.")
    if not Z.dtype == "float64" or not reshapedX.dtype == "float64":
        raise ValueError("reshapedX, Z must be float64.")
    if not S.dtype == "float64":
        raise ValueError("S must be float64.")

    cdef uintptr_t addr_reshapedCopy = reshapedXCopy.data.ptr
    cdef double *reshapedXCopyPtr = <double*>addr_reshapedCopy
    cdef uintptr_t addr_preSumFeats = preSumFeats.data.ptr
    cdef double *preSumFeatsPtr = <double*>addr_preSumFeats
 
    cdef uintptr_t addr_radem = radem.data.ptr
    cdef int8_t *radem_ptr = <int8_t*>addr_radem


    startPosition, cutoff = 0, reshapedX.shape[2]
    scalingTerm = np.sqrt(1 / <double>radem.shape[2])

    for i in range(num_repeats):
        preSumFeats[:] = reshapedX
        errCode = doublePolyFHTPrep_(radem_ptr,
                    preSumFeatsPtr, reshapedX.shape[0], reshapedX.shape[1], 
                    reshapedX.shape[2], radem.shape[2], i * reshapedX.shape[2], 0)
        if errCode.decode("UTF-8") != "no_error":
            raise Exception("Fatal error encountered while performing graph convolution.")
        preSumFeats *= S[0,None,(i * reshapedX.shape[2]):((i+1) * reshapedX.shape[2])]
        for j in range(1, polydegree):
            reshapedXCopy[:] = reshapedX
            errCode = doublePolyFHTPrep_(radem_ptr,
                    reshapedXCopyPtr, reshapedX.shape[0], reshapedX.shape[1], 
                    reshapedX.shape[2], radem.shape[2], i * reshapedX.shape[2], j)
            reshapedXCopy *= S[j,None,(i * reshapedX.shape[2]):((i+1) * reshapedX.shape[2])]
            preSumFeats *= reshapedXCopy
        Z[:,startPosition:cutoff] = cp.sum(preSumFeats, axis=1)

        cutoff += reshapedX.shape[2]
        startPosition += reshapedX.shape[2]

    Z *= scalingTerm
