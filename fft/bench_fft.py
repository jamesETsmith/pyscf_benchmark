import os
import time
import numpy as np
import pandas as pd
from importlib import reload
import pyscf
from pyscf import __config__
from pyscf.pbc import tools


ALLOWED_ENGINES = ["FFTW", "NUMPY", "NUMPY+BLAS", "BLAS"]


def bench_fft_engine(method: str, mesh_size: int):

    # Check inputs (in case this is used as solo)
    if method not in ALLOWED_ENGINES:
        msg = f"{method} is not an allowd FFT engine ({ALLOWED_ENGINES})"
        raise ValueError(msg)

    # Set the engine
    __config__.pbc_tools_pbc_fft_engine = method
    reload(pyscf.pbc.tools.pbc)  # reload so we see updated config

    a = np.random.random([2, mesh_size, mesh_size, mesh_size])

    # Time FFT
    _t0 = time.perf_counter()
    tools.fft(a, [mesh_size, mesh_size, mesh_size])
    total_time = time.perf_counter() - _t0

    print(f"FFT TIME {total_time}")

    return total_time


def bench_all_fft_engines(mesh_size: int):
    # Setup data directory
    os.makedirs("_data", exist_ok=True)
    filename = "_data/bench_fft_data.csv"

    # Read in old data so we can append if necessary
    if os.path.exists(filename):
        data = pd.read_csv(filename)
        print(data)
        data = data.to_dict(orient="list")
    else:
        data = {
            "FFT Engine": [],
            "Time (s)": [],
            "OMP_NUM_THREADS": [],
            "MESH_SIZE": [],
        }

    # Iterate through all engines
    for eng in ALLOWED_ENGINES:
        total_time = bench_fft_engine(eng, mesh_size=mesh_size)
        data["FFT Engine"].append(eng)
        data["Time (s)"].append(total_time)
        data["OMP_NUM_THREADS"].append(int(os.environ["OMP_NUM_THREADS"]))
        data["MESH_SIZE"].append(mesh_size)

    pd.DataFrame(data).to_csv(filename, index=False)

    return data


if __name__ == "__main__":
    # Read CLIs
    import argparse

    parser = argparse.ArgumentParser(
        description="Benchmark the FFT engine options for PySCF"
    )
    parser.add_argument(
        "--mesh_size",
        type=int,
        required=True,
        help="The size of the mesh used in the problem. The larger the mesh, the more memory and operations FFT requires.",
    )
    args = parser.parse_args()
    mesh_size = args.mesh_size

    # For debugging
    # bench_fft_engine("FFTW", mesh_size)
    # bench_fft_engine("NUMPY", mesh_size)
    # bench_fft_engine("NUMPY+BLAS", mesh_size)
    # bench_fft_engine("BLAS", mesh_size)

    data = bench_all_fft_engines(mesh_size)
