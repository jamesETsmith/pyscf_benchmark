import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


df = pd.read_csv("_data/bench_solver_data.csv")
filename = "bench_solver_report"
size = df["Matrix Size"]
if not np.all(size == size[0]):
    print(
        "WARNING: NOT ALL MATRIX SIZES IN DATA FILE ARE THE SAME. MAKE SURE YOUR RUNS ARE CONSISTENT."
    )

plt.figure(figsize=(10, 6))
sns.set_theme(context="talk", style="ticks")
plt.title(f"SciPy Solver Benchmark for Matrix Size={size[0]}")

g = sns.barplot(data=df, hue="Method", y="Time (s)", x="OMP_NUM_THREADS", log=True)
g.legend(loc="center left", bbox_to_anchor=(1, 0.5))

os.makedirs("_figures", exist_ok=True)
plt.tight_layout()
plt.savefig(f"_figures/{filename}.svg")
# plt.savefig(f"_figures/{filename}.png", dpi=600)
