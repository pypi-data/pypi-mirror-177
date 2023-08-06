#!/bin/bash

nvcc -rdc=true --compiler-options '-fPIC' --expt-relaxed-constexpr  -c -o double_arrop_temp.o double_array_operations.cu
nvcc -rdc=true --compiler-options '-fPIC' --expt-relaxed-constexpr  -c -o float_arrop_temp.o float_array_operations.cu
nvcc -rdc=true --compiler-options '-fPIC' --expt-relaxed-constexpr  -c -o polyfht_temp.o poly_fht.cu
nvcc -rdc=true --compiler-options '-fPIC' --expt-relaxed-constexpr  -c -o conv_temp.o convolution.cu

nvcc -dlink --compiler-options '-fPIC' -o double_array_operations.o double_arrop_temp.o -lcudart
nvcc -dlink --compiler-options '-fPIC' -o float_array_operations.o float_arrop_temp.o -lcudart
nvcc -dlink --compiler-options '-fPIC' -o convolution.o conv_temp.o -lcudart
nvcc -dlink --compiler-options '-fPIC' -o poly_fht.o polyfht_temp.o -lcudart

ar cru libarray_operations.a double_array_operations.o float_array_operations.o double_arrop_temp.o float_arrop_temp.o conv_temp.o convolution.o polyfht_temp.o poly_fht.o
ranlib libarray_operations.a
rm -f double_arrop_temp.o float_arrop_temp.o double_array_operations.o float_array_operations.o conv_temp.o convolution.o
rm -f poly_fht.o polyfht_temp.o
