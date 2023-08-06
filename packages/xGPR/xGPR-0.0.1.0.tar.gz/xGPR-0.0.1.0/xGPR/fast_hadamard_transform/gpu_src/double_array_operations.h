#ifndef DOUBLE_CUDA_ARRAY_OPERATIONS_H
#define DOUBLE_CUDA_ARRAY_OPERATIONS_H

extern "C" const char *doubleCudaSORF3d_(double *npArray, 
                    int8_t *radem, int dim0, int dim1,
                    int dim2);
extern "C" const char *doubleCudaSRHT2d_(double *npArray, 
                    int8_t *radem, int dim0, int dim1);
void doubleCudaHTransform3d_(double *cArray,
		int dim0, int dim1, int dim2);
void doubleCudaHTransform2d_(double *cArray,
		int dim0, int dim1);
int getNumBlocksDoubleTransform(int arrsize, int divisor);


#endif
