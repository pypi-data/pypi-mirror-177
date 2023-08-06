/*!
 * # poly_fht_operations.c
 *
 * This module performs operations unique to the polynomial kernel
 * in xGPR. It includes the following functions:
 * + floatPolyFHTPrep_
 * Performs a 1d orthogonal random features based transformation
 * on the input array using a specified number of threads. Floats only.
 * + doublePolyFHTPrep_
 * Performs a 1d orthogonal random features based transformation
 * on the input array using a specified number of threads. Doubles only.
 * + ThreadPolyFHTFloat
 * Called once by floatPolyFHTPrep_ for each thread.
 * + ThreadPolyFHTDouble
 * Called once by doublePolyFHTPrep_ for each thread.
 *
 * Functions from float_ or double_ array_operations.c are called to perform the
 * Hadamard transform and diagonal matrix multiplications.
 */
#include <Python.h>
#include <numpy/arrayobject.h>
#include <pthread.h>
#include <math.h>
#include <stdio.h>
#include <string.h>
#include "thread_args.h"
#include "poly_fht_operations.h"
#include "double_array_operations.h"
#include "float_array_operations.h"


/*!
 * # floatPolyFHTPrep_
 *
 * Performs orthogonal random features based transformation
 * as prep for the caller will perform, on an input array of floats.
 * It is assumed that caller
 * has checked dimensions and they are all correct.
 *
 * ## Args:
 *
 * + `radem` The stacks of diagonal matrices used in
 * the transform. Must be of shape (3 * polydegree x 1 x m * C) where m is
 * an integer that indicates the number of times we must repeat
 * the operation to generate the requested number of features.
 * + `reshapedX` Pointer to the first element of the array that will
 * be used for the convolution. A copy of this array is modified
 * rather than the original. Shape is (N x D x C). C must be a power
 * of 2.
 * + `numThreads` The number of threads to use
 * + `reshapedDim0` The first dimension of reshapedX
 * + `reshapedDim1` The second dimension of reshapedX
 * + `reshapedDim2` The last dimension of reshapedX
 * + `numFreqs` The number of frequencies to sample. Must == Z.shape[1].
 * numFreqs must be equal to shape[2] of radem and shape[0] of S.
 * + `startPosition` An int indicating where to start in the
 * radem array.
 * + `rademStartPosition` An int indicating which row of the radem
 * array to use; unique for the polynomial kernel.
 *
 * ## Returns:
 * "error" if an error, "no_error" otherwise.
 */
const char *floatPolyFHTPrep_(int8_t *radem, float *reshapedX,
            int numThreads, int reshapedDim0,
            int reshapedDim1, int reshapedDim2, int numFreqs,
            int startPosition, int rademStartPosition)
{
    struct ThreadConv1dFloatArgs *th_args = malloc(numThreads * sizeof(struct ThreadConv1dFloatArgs));
    if (th_args == NULL){
        PyErr_SetString(PyExc_ValueError, "Memory allocation unsuccessful! If you don't know what that means..."
                "hint: it's really bad news...");
        return "error";
    }
    //Note the variable length arrays, which are fine with gcc BUT may be a problem for some older
    //C++ compilers.
    int i, threadFlags[numThreads];
    int iret[numThreads];
    void *retval[numThreads];
    pthread_t thread_id[numThreads];
    int chunkSize = (reshapedDim0 + numThreads - 1) / numThreads;
    int repeat;
   
    //We assume here that ZDim1 is an integer multiple
    //of reshapedDim2 (caller must check this -- the
    //Cython wrapper does). 
    for (i=0; i < numThreads; i++){
        th_args[i].startPosition = startPosition;
        th_args[i].startRow = i * chunkSize;
        th_args[i].endRow = (i + 1) * chunkSize;
        if (th_args[i].endRow > reshapedDim0)
            th_args[i].endRow = reshapedDim0;
        th_args[i].reshapedDim1 = reshapedDim1;
        th_args[i].reshapedDim2 = reshapedDim2;
        th_args[i].rademArray = radem + rademStartPosition * 3 * numFreqs;
        th_args[i].reshapedXArray = reshapedX;
        th_args[i].numFreqs = numFreqs;
    }
    for (i=0; i < numThreads; i++){
        iret[i] = pthread_create(&thread_id[i], NULL, ThreadPolyFHTFloat, &th_args[i]);
        if (iret[i]){
            PyErr_SetString(PyExc_ValueError, "fastHadamardTransform failed to create a thread!");
            return "error";
        }
    }
    for (i=0; i < numThreads; i++)
        threadFlags[i] = pthread_join(thread_id[i], &retval[i]);
    return "no_error";
}



/*!
 * # doublePolyFHTPrep_
 *
 * Performs orthogonal random features based transformation
 * as prep for the caller will perform, on an input array of floats.
 * It is assumed that caller
 * has checked dimensions and they are all correct.
 *
 * ## Args:
 *
 * + `radem` The stacks of diagonal matrices used in
 * the transform. Must be of shape (3 * polydegree x 1 x m * C) where m is
 * an integer that indicates the number of times we must repeat
 * the operation to generate the requested number of features.
 * + `reshapedX` Pointer to the first element of the array that will
 * be used for the convolution. A copy of this array is modified
 * rather than the original. Shape is (N x D x C). C must be a power
 * of 2.
 * + `numThreads` The number of threads to use
 * + `reshapedDim0` The first dimension of reshapedX
 * + `reshapedDim1` The second dimension of reshapedX
 * + `reshapedDim2` The last dimension of reshapedX
 * + `numFreqs` The number of frequencies to sample. Must == Z.shape[1].
 * numFreqs must be equal to shape[2] of radem and shape[0] of S.
 * + `startPosition` An int indicating where to start in the
 * radem array.
 * + `rademStartPosition` An int indicating which row of the radem
 * array to use; unique for the polynomial kernel.
 *
 * ## Returns:
 * "error" if an error, "no_error" otherwise.
 */
const char *doublePolyFHTPrep_(int8_t *radem, double *reshapedX,
            int numThreads, int reshapedDim0,
            int reshapedDim1, int reshapedDim2, int numFreqs,
            int startPosition, int rademStartPosition)
{
    struct ThreadConv1dDoubleArgs *th_args = malloc(numThreads *
            sizeof(struct ThreadConv1dDoubleArgs));
    if (th_args == NULL){
        PyErr_SetString(PyExc_ValueError, "Memory allocation unsuccessful! If you don't know what that means..."
                "hint: it's really bad news...");
        return "error";
    }
    //Note the variable length arrays, which are fine with gcc BUT may be a problem for some older
    //C++ compilers.
    int i, threadFlags[numThreads];
    int iret[numThreads];
    void *retval[numThreads];
    pthread_t thread_id[numThreads];
    int chunkSize = (reshapedDim0 + numThreads - 1) / numThreads;
   
    //We assume here that ZDim1 is an integer multiple
    //of reshapedDim2 (caller must check this -- the
    //Cython wrapper does). 
    for (i=0; i < numThreads; i++){
        th_args[i].startPosition = startPosition;
        th_args[i].startRow = i * chunkSize;
        th_args[i].endRow = (i + 1) * chunkSize;
        if (th_args[i].endRow > reshapedDim0)
            th_args[i].endRow = reshapedDim0;
        th_args[i].reshapedDim1 = reshapedDim1;
        th_args[i].reshapedDim2 = reshapedDim2;
        th_args[i].rademArray = radem + rademStartPosition * 3 * numFreqs;
        th_args[i].reshapedXArray = reshapedX;
        th_args[i].numFreqs = numFreqs;
    }
    for (i=0; i < numThreads; i++){
        iret[i] = pthread_create(&thread_id[i], NULL, ThreadPolyFHTDouble, &th_args[i]);
        if (iret[i]){
            PyErr_SetString(PyExc_ValueError, "fastHadamardTransform failed to create a thread!");
            return "error";
        }
    }
    for (i=0; i < numThreads; i++)
        threadFlags[i] = pthread_join(thread_id[i], &retval[i]);
    return "no_error";
}


/*!
 * # ThreadPolyFHTFloat
 *
 * Performs orthogonal random features based transform
 * for a single thread. reshapedXCopy is split up into
 * num_threads chunks each with a start and end row and each
 * thread modifies the corresponding rows of reshapedXCopy and Z.
 * For input float arrays only.
 *
 * ## Args:
 * + `sharedArgs` A void pointer to a ThreadConv1dFloatArgs struct
 * containing pointers to the arrays needed to execute the
 * transform, the start and end rows etc.
 */
void *ThreadPolyFHTFloat(void *sharedArgs){
    struct ThreadConv1dFloatArgs *thArgs = (struct ThreadConv1dFloatArgs *)sharedArgs;
    
    floatConv1dMultiplyByDiagonalMat(thArgs->reshapedXArray,
                    thArgs->rademArray, thArgs->startRow,
                    thArgs->endRow, thArgs->reshapedDim1, 
                    thArgs->reshapedDim2, thArgs->startPosition);
    floatTransformRows3D(thArgs->reshapedXArray, thArgs->startRow,
                    thArgs->endRow, thArgs->reshapedDim1, 
                    thArgs->reshapedDim2);
    floatConv1dMultiplyByDiagonalMat(thArgs->reshapedXArray,
                    thArgs->rademArray + thArgs->numFreqs,
                    thArgs->startRow, thArgs->endRow,
                    thArgs->reshapedDim1, thArgs->reshapedDim2,
                    thArgs->startPosition);
    floatTransformRows3D(thArgs->reshapedXArray, thArgs->startRow,
                    thArgs->endRow, thArgs->reshapedDim1, 
                    thArgs->reshapedDim2);
    
    floatConv1dMultiplyByDiagonalMat(thArgs->reshapedXArray,
                    thArgs->rademArray + 2 * thArgs->numFreqs,
                    thArgs->startRow, thArgs->endRow,
                    thArgs->reshapedDim1, thArgs->reshapedDim2,
                    thArgs->startPosition);
    floatTransformRows3D(thArgs->reshapedXArray, thArgs->startRow,
                    thArgs->endRow, thArgs->reshapedDim1, 
                    thArgs->reshapedDim2);
    return NULL;
}




/*!
 * # ThreadPolyFHTDouble
 *
 * Performs orthogonal random features based transform
 * for a single thread. reshapedXCopy is split up into
 * num_threads chunks each with a start and end row and each
 * thread modifies the corresponding rows of reshapedXCopy and Z.
 * For input double arrays only.
 *
 * ## Args:
 * + `sharedArgs` A void pointer to a ThreadConv1dDoubleArgs struct
 * containing pointers to the arrays needed to execute the
 * transform, the start and end rows etc.
 */
void *ThreadPolyFHTDouble(void *sharedArgs){
    struct ThreadConv1dDoubleArgs *thArgs = (struct ThreadConv1dDoubleArgs *)sharedArgs;
    
    doubleConv1dMultiplyByDiagonalMat(thArgs->reshapedXArray,
                    thArgs->rademArray, thArgs->startRow,
                    thArgs->endRow, thArgs->reshapedDim1, 
                    thArgs->reshapedDim2, thArgs->startPosition);
    doubleTransformRows3D(thArgs->reshapedXArray, thArgs->startRow,
                    thArgs->endRow, thArgs->reshapedDim1, 
                    thArgs->reshapedDim2);
    doubleConv1dMultiplyByDiagonalMat(thArgs->reshapedXArray,
                    thArgs->rademArray + thArgs->numFreqs,
                    thArgs->startRow, thArgs->endRow,
                    thArgs->reshapedDim1, thArgs->reshapedDim2,
                    thArgs->startPosition);
    doubleTransformRows3D(thArgs->reshapedXArray, thArgs->startRow,
                    thArgs->endRow, thArgs->reshapedDim1, 
                    thArgs->reshapedDim2);
    
    doubleConv1dMultiplyByDiagonalMat(thArgs->reshapedXArray,
                    thArgs->rademArray + 2 * thArgs->numFreqs,
                    thArgs->startRow, thArgs->endRow,
                    thArgs->reshapedDim1, thArgs->reshapedDim2,
                    thArgs->startPosition);
    doubleTransformRows3D(thArgs->reshapedXArray, thArgs->startRow,
                    thArgs->endRow, thArgs->reshapedDim1, 
                    thArgs->reshapedDim2);
    return NULL;
}
