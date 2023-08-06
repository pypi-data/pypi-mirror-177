#ifndef FLOAT_ARRAY_OPERATIONS_H
#define FLOAT_ARRAY_OPERATIONS_H

#include <Python.h>
#include <numpy/arrayobject.h>

void floatTransformRows3D(float *arrayStart, int startRow, int endRow,
                    int dim1, int dim2);
void floatTransformRows2D(float *arrayStart, int startRow, int endRow,
                    int dim1);

void floatMultiplyByDiagonalRademacherMat(float *arrayStart,
                    int8_t *rademArrayStart,
                    int dim1, int dim2,
                    int startRow, int endRow);
void floatMultiplyByDiagonalRademacherMat2D(float *arrayStart,
                    int8_t *rademArrayStart,
                    int dim1, int startRow, int endRow);
void floatConv1dMultiplyByDiagonalMat(float *reshapedX,
                        int8_t *rademArray, int startRow,
                        int endRow, int reshapedDim1,
                        int reshapedDim2, int startPosition);

#endif
