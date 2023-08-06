/*
* Contains functions needed to run FHT for the polynomial kernel on GPU.
* The input array should already live on GPU.
* The Hadamard transforms are performed using functions from float or double
* array_operations.cu, the diagonal matrix multiplication is slightly different
* and so is implemented here.
*/
#include <cuda.h>
#include <cuda_runtime.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "double_array_operations.h"
#include "float_array_operations.h"
#include "poly_fht.h"

#define DEFAULT_THREADS_PER_BLOCK 256



//Performs an elementwise multiplication of a row of a [1,1,P x S] array against the
//[N,M,S] input array. Note that the dimensions must be checked before calling
//-- done by the wrapper -- and that only S elements of the [1, 1, P x S] array are used.
__global__ void floatPolyFHTMultiplyByDiagonalMat(float *cArray, int8_t *rademArray,
			int dim2, int columnStartPosition, int numElements, float normConstant)
{
    int j = blockDim.x * blockIdx.x + threadIdx.x;
    int8_t *rVal = rademArray + columnStartPosition + (j & (dim2 - 1));
    
    if (j < numElements)
        cArray[j] = cArray[j] * *rVal * normConstant;
}



//Performs an elementwise multiplication of a row of a [1,1,P x S] array against the
//[N,M,S] input array. Note that the dimensions must be checked before calling
//-- done by the wrapper -- and that only S elements of the [1, 1, P x S] array are used.
__global__ void doublePolyFHTMultiplyByDiagonalMat(double *cArray, int8_t *rademArray,
			int dim2, int columnStartPosition, int numElements, double normConstant)
{
    int j = blockDim.x * blockIdx.x + threadIdx.x;
    int8_t *rVal = rademArray + columnStartPosition + (j & (dim2 - 1));
    
    if (j < numElements)
        cArray[j] = cArray[j] * *rVal * normConstant;
}



//This function performs the FHT operation for the polynomial kernel
//when the input is an arrray of floats.
//Note that reshapedX must have the same size across the
//last two dimensions as radem and its last dimension must
//be a power of two -- if those conditions are not met, you may
//get an unpredictable result! The Cython wrapper checks all
//of these criteria.
//
//All of these arrays are already expected to "live" on GPU.
const char *floatPolyFHTPrep_(int8_t *radem, float *reshapedX, int reshapedDim0, 
                int reshapedDim1, int reshapedDim2, int numFreqs,
                int columnStartPosition, int rowStartPosition){

    int numElements = reshapedDim0 * reshapedDim1 * reshapedDim2;
    int rowOffset;
    //This is the Hadamard normalization constant.
    float normConstant = log2(reshapedDim2) / 2;
    normConstant = 1 / pow(2, normConstant);
    int blocksPerGrid = (numElements + DEFAULT_THREADS_PER_BLOCK - 1) / 
                DEFAULT_THREADS_PER_BLOCK;
    
    //Multiply by radem row 1.
    rowOffset = rowStartPosition * 3 * numFreqs;
    floatPolyFHTMultiplyByDiagonalMat<<<blocksPerGrid, DEFAULT_THREADS_PER_BLOCK>>>(reshapedX, 
                        radem + rowOffset, reshapedDim2, columnStartPosition, numElements,
                        normConstant);
    //First H-transform.
    floatCudaHTransform3d_(reshapedX, reshapedDim0, reshapedDim1, reshapedDim2);

    //Multiply by second row of radem.
    rowOffset += numFreqs;
    floatPolyFHTMultiplyByDiagonalMat<<<blocksPerGrid, DEFAULT_THREADS_PER_BLOCK>>>(reshapedX, 
                        radem + rowOffset, reshapedDim2, columnStartPosition,
                        numElements, normConstant);
    //Second H-transform.
    floatCudaHTransform3d_(reshapedX, reshapedDim0, reshapedDim1, reshapedDim2);
        
    //Multiply by third row of radem.
    rowOffset += numFreqs;
    floatPolyFHTMultiplyByDiagonalMat<<<blocksPerGrid, DEFAULT_THREADS_PER_BLOCK>>>(reshapedX, 
                        radem + rowOffset, reshapedDim2, columnStartPosition,
                        numElements, normConstant);
    //Third H-transform.
    floatCudaHTransform3d_(reshapedX, reshapedDim0, reshapedDim1, reshapedDim2);
    //All operations are in place, no need to return anything except a 
    //no error message. TODO: check the cuda kernels for errors and add error
    //handling.
    return "no_error";
}



//This function performs the FHT operation for the polynomial kernel
//when the input is an arrray of doubles.
//Note that reshapedX must have the same size across the
//last two dimensions as radem and its last dimension must
//be a power of two -- if those conditions are not met, you may
//get an unpredictable result! The Cython wrapper checks all
//of these criteria.
//
//All of these arrays are already expected to "live" on GPU.
const char *doublePolyFHTPrep_(int8_t *radem, double *reshapedX, int reshapedDim0, 
                int reshapedDim1, int reshapedDim2, int numFreqs,
                int columnStartPosition, int rowStartPosition){

    int numElements = reshapedDim0 * reshapedDim1 * reshapedDim2;
    int rowOffset;
    //This is the Hadamard normalization constant.
    double normConstant = log2(reshapedDim2) / 2;
    normConstant = 1 / pow(2, normConstant);
    int blocksPerGrid = (numElements + DEFAULT_THREADS_PER_BLOCK - 1) / 
                DEFAULT_THREADS_PER_BLOCK;
    
    //Multiply by radem row 1.
    rowOffset = rowStartPosition * 3 * numFreqs;
    doublePolyFHTMultiplyByDiagonalMat<<<blocksPerGrid, DEFAULT_THREADS_PER_BLOCK>>>(reshapedX, 
                        radem + rowOffset, reshapedDim2, columnStartPosition, numElements,
                        normConstant);
    //First H-transform.
    doubleCudaHTransform3d_(reshapedX, reshapedDim0, reshapedDim1, reshapedDim2);

    //Multiply by second row of radem.
    rowOffset += numFreqs;
    doublePolyFHTMultiplyByDiagonalMat<<<blocksPerGrid, DEFAULT_THREADS_PER_BLOCK>>>(reshapedX, 
                        radem + rowOffset, reshapedDim2, columnStartPosition,
                        numElements, normConstant);
    //Second H-transform.
    doubleCudaHTransform3d_(reshapedX, reshapedDim0, reshapedDim1, reshapedDim2);
        
    //Multiply by third row of radem.
    rowOffset += numFreqs;
    doublePolyFHTMultiplyByDiagonalMat<<<blocksPerGrid, DEFAULT_THREADS_PER_BLOCK>>>(reshapedX, 
                        radem + rowOffset, reshapedDim2, columnStartPosition,
                        numElements, normConstant);
    //Third H-transform.
    doubleCudaHTransform3d_(reshapedX, reshapedDim0, reshapedDim1, reshapedDim2);
    //All operations are in place, no need to return anything except a 
    //no error message. TODO: check the cuda kernels for errors and add error
    //handling.
    return "no_error";
}
