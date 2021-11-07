import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


df = pd.read_csv("_data/bench_fft_data.csv")
filename = "bench_fft_report"
mesh_sizes = df["MESH_SIZE"]
if not np.all(mesh_sizes == mesh_sizes[0]):
    print(
        "WARNING: NOT ALL MESH SIZES IN DATA FILE ARE THE SAME. MAKE SURE YOUR RUNS ARE CONSISTENT."
    )

plt.figure(figsize=(10, 6))
sns.set_theme(context="talk", style="ticks")
plt.title(f"FFT Engine Benchmark for MESH_SIZE={mesh_sizes[0]}")

g = sns.barplot(data=df, hue="FFT Engine", y="Time (s)", x="OMP_NUM_THREADS")
g.legend(loc="center left", bbox_to_anchor=(1, 0.5))

os.makedirs("_figures", exist_ok=True)
plt.tight_layout()
plt.savefig(f"_figures/{filename}.svg")
plt.savefig(f"_figures/{filename}.png", dpi=600)
