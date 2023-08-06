#ifndef CUDA_POLY_FHT_PREP_H
#define CUDA_POLY_FHT_PREP_H

const char *floatPolyFHTPrep_(int8_t *radem, float *reshapedX, int reshapedDim0,
                int reshapedDim1, int reshapedDim2, int numFreqs,
                int columnStartPosition, int rowStartPosition);

const char *doublePolyFHTPrep_(int8_t *radem, double *reshapedX, int reshapedDim0,
                int reshapedDim1, int reshapedDim2, int numFreqs,
                int columnStartPosition, int rowStartPosition);

#endif
