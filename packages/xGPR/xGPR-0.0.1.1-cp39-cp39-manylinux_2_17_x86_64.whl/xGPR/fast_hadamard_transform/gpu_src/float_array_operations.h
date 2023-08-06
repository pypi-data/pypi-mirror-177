#ifndef FLOAT_CUDA_ARRAY_OPERATIONS_H
#define FLOAT_CUDA_ARRAY_OPERATIONS_H

extern "C" const char *floatCudaSORF3d_(float *npArray, 
                    int8_t *radem, int dim0, int dim1,
                    int dim2);
extern "C" const char *floatCudaSRHT2d_(float *npArray, 
                    int8_t *radem, int dim0, int dim1);
void floatCudaHTransform3d_(float *cArray,
		int dim0, int dim1, int dim2);
void floatCudaHTransform2d_(float *cArray,
		int dim0, int dim1);
int getNumBlocksFloatTransform(int arrsize, int divisor);


#endif
