#!/bin/env bash

rm -f _data/bench_fft_data.csv

N_REPEAT=10
MESH_SIZE=400

for NTHREADS in 1 2 4 8 16
do
    for _ in $(seq $N_REPEAT)
    do
	# Some MKL builds may need to preload core and sequential to avoid the error
	# "undefined symbol: mkl_sparse_optimize_bsr_trsm_i8"
	# LD_PRELOAD=$MKLROOT/lib/intel64/libmkl_core.so:$MKLROOT/lib/intel64/libmkl_sequential.so \
	MKL_NUM_THREADS=$NTHREADS OMP_NUM_THREADS=$NTHREADS \
    python bench_fft.py --mesh_size=${MESH_SIZE}
    done
done
