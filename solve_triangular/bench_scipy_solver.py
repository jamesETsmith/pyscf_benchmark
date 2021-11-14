import os
import time
import numpy as np
import pandas as pd
from scipy.linalg import solve_triangular, solve

ALLOWED_SOLVERS = ["general", "hermitian", "symmetric", "triangular"]


def _bench_single_solver(size: int, method: str):
    # Setup problem
    a = np.random.rand(size, size)
    a = a + a.T
    b = np.random.rand(size)

    # Run benchmark
    _t0 = time.perf_counter()

    if method == "triangular":
        solve_triangular(a, b, lower=True, overwrite_b=True)
    elif method in ALLOWED_SOLVERS:
        solve(a, b, assume_a=method[:3])
    else:
        raise ValueError(f"Method ({method}) not supported!")

    t_solve = time.perf_counter() - _t0
    return t_solve


def bench_scipy_solver(size: int):
    # Setup data directory
    os.makedirs("_data", exist_ok=True)
    filename = "_data/bench_solver_data.csv"

    if os.path.exists(filename):
        data = pd.read_csv(filename)
        print(data)
        data = data.to_dict(orient="list")
    else:
        data = {"Time (s)": [], "OMP_NUM_THREADS": [], "Matrix Size": [], "Method": []}

    for solver in ALLOWED_SOLVERS:
        t_solve = _bench_single_solver(size, solver)
        data["Time (s)"].append(t_solve)
        data["Matrix Size"].append(size)
        data["OMP_NUM_THREADS"].append(int(os.environ["OMP_NUM_THREADS"]))
        data["Method"].append(solver)

    pd.DataFrame(data).to_csv(filename, index=False)
    return data


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Benchmark the SciPy triangular solver used in PySCF"
    )
    parser.add_argument(
        "--size",
        type=int,
        required=True,
        help="Size of the system to solve. A size of N means, we're solving a matrix of size (N,N).",
    )
    args = parser.parse_args()

    # Run bench
    bench_scipy_solver(args.size)
