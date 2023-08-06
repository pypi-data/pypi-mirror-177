#ifndef DOUBLE_ARRAY_OPERATIONS_H
#define DOUBLE_ARRAY_OPERATIONS_H

#include <Python.h>
#include <numpy/arrayobject.h>

void doubleTransformRows3D(double *arrayStart, int startRow, int endRow,
                    int dim1, int dim2);
void doubleTransformRows2D(double *arrayStart, int startRow, int endRow,
                    int dim1);

void doubleMultiplyByDiagonalRademacherMat(double *arrayStart,
                    int8_t *rademArrayStart,
                    int dim1, int dim2,
                    int startRow, int endRow);
void doubleMultiplyByDiagonalRademacherMat2D(double *arrayStart,
                    int8_t *rademArrayStart,
                    int dim1, int startRow, int endRow);
void doubleConv1dMultiplyByDiagonalMat(double *reshapedX,
                        int8_t *rademArray, int startRow,
                        int endRow, int reshapedDim1,
                        int reshapedDim2, int startPosition);

#endif
