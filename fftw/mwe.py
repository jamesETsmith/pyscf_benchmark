import os
import time
import numpy as np
import pandas as pd
from importlib import reload

ALLOWED_ENGINES = ["FFTW", "NUMPY", "NUMPY+BLAS", "BLAS"]
SYSTEMS = {
    "small": {"atom": "He 0 0 0; He 0.75 0 0;", "basis": "gth-dzvp"},
    "medium": {"atom": "Ne 0 0 0; Ne 0.75 0 0;", "basis": "gth-tzvp"},
    "large": {"atom": "Ar 0 0 0; Ar 0.75 0 0;", "basis": "gth-tzvp"},
}


def bench_fft_engine(method: str):

    if method not in ALLOWED_ENGINES:
        msg = f"{method} is not an allowd FFT engine ({ALLOWED_ENGINES})"
        raise ValueError(msg)

    import pyscf
    from pyscf import __config__

    __config__.pbc_tools_pbc_fft_engine = method

    from pyscf.pbc import gto, scf

    reload(pyscf.pbc.tools.pbc)

    atom = "Ar 0 0 0; Ar 0.75 0 0"
    a = np.eye(3) * 3
    basis = "gth-tzvp"
    pseudo = "gth-pade"

    cell = gto.Cell(atom=atom, a=a, basis=basis, pseudo=pseudo)
    cell.mesh = [21, 21, 21]
    cell.build()
    cell.verbose = 0

    kmesh = [2, 2, 1]
    kpts = cell.make_kpts(kmesh)

    # Time SCF
    _t0 = time.perf_counter()

    mf = scf.KRHF(cell, kpts)
    mf.kernel()

    total_time = time.perf_counter() - _t0
    print(f"SCF TIME {total_time}")
    del gto, scf
    return total_time


def bench_all_fft_engines():
    filename = "bench_fft_data.csv"

    if os.path.exists(filename):
        data = pd.read_csv(filename).to_dict(orient="list")
        print(data)
    else:
        data = {
            "FFT Engine": [],
            "Time (s)": [],
            "OMP_NUM_THREADS": [],
        }

    for eng in ALLOWED_ENGINES:
        total_time = bench_fft_engine(eng)
        data["FFT Engine"].append(eng)
        data["Time (s)"].append(total_time)
        data["OMP_NUM_THREADS"].append(int(os.environ["OMP_NUM_THREADS"]))

    pd.DataFrame(data).to_csv(filename, index=False)

    return data


if __name__ == "__main__":
    # bench_fft_engine("FFTW")
    # bench_fft_engine("NUMPY")
    # bench_fft_engine("NUMPY+BLAS")
    # bench_fft_engine("BLAS")

    data = bench_all_fft_engines()
