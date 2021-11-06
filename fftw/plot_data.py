import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


df = pd.read_csv("_data/bench_fft_data.csv")
filename = "bench_fft_report"

plt.figure(figsize=(10, 6))
sns.set_theme(context="talk", style="ticks")

g = sns.boxplot(data=df, hue="FFT Engine", y="Time (s)", x="OMP_NUM_THREADS")
g.legend(loc="center left", bbox_to_anchor=(1, 0.5))

os.makedirs("_figures", exist_ok=True)
plt.tight_layout()
plt.savefig(f"_figures/{filename}.svg")
plt.savefig(f"_figures/{filename}.png", dpi=600)
