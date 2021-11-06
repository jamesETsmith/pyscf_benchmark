import os
import time
import numpy as np
import pandas as pd
from importlib import reload
import pyscf
from pyscf import __config__
from pyscf.pbc import tools


ALLOWED_ENGINES = ["FFTW", "NUMPY", "NUMPY+BLAS", "BLAS"]
N_SIZE = 600


def bench_fft_engine(method: str):

    # Check inputs (in case this is used as solo)
    if method not in ALLOWED_ENGINES:
        msg = f"{method} is not an allowd FFT engine ({ALLOWED_ENGINES})"
        raise ValueError(msg)

    # Set the engine
    __config__.pbc_tools_pbc_fft_engine = method
    reload(pyscf.pbc.tools.pbc)  # reload so we see updated config

    # Time FFT
    _t0 = time.perf_counter()

    a = np.random.random([2, N_SIZE, N_SIZE, N_SIZE])
    tools.fft(a, [N_SIZE, N_SIZE, N_SIZE])

    total_time = time.perf_counter() - _t0
    print(f"FFT TIME {total_time}")

    return total_time


def bench_all_fft_engines():
    # Setup data directory
    os.makedirs("_data", exist_ok=True)
    filename = "_data/bench_fft_data.csv"

    # Read in old data so we can append if necessary
    if os.path.exists(filename):
        data = pd.read_csv(filename).to_dict(orient="list")
        print(data)
    else:
        data = {
            "FFT Engine": [],
            "Time (s)": [],
            "OMP_NUM_THREADS": [],
        }

    # Iterate through all engines
    for eng in ALLOWED_ENGINES:
        total_time = bench_fft_engine(eng)
        data["FFT Engine"].append(eng)
        data["Time (s)"].append(total_time)
        data["OMP_NUM_THREADS"].append(int(os.environ["OMP_NUM_THREADS"]))

    pd.DataFrame(data).to_csv(filename, index=False)

    return data


if __name__ == "__main__":
    # For debugging
    # bench_fft_engine("FFTW")
    # bench_fft_engine("NUMPY")
    # bench_fft_engine("NUMPY+BLAS")
    # bench_fft_engine("BLAS")

    data = bench_all_fft_engines()
