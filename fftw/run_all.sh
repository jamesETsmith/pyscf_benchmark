#!/bin/env bash

rm bench_fft_data.csv

for NTHREADS in 1 2 4 8 16
do
    OMP_NUM_THREADS=$NTHREADS python mwe.py
done