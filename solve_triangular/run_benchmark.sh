#!/bin/env bash

rm -f _data/bench_solver_data.csv

N_REPEAT=10
SIZE=10000

for NTHREADS in 1 2 4 8 16
do
    for _ in $(seq $N_REPEAT)
    do
	MKL_NUM_THREADS=$NTHREADS OMP_NUM_THREADS=$NTHREADS \
    python bench_scipy_solver.py --size=${SIZE}
    done
done
