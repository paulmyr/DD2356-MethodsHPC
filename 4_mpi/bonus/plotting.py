import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter

processes = np.array([1, 2, 4, 8, 16, 32, 64])
parallel_runtimes = np.array([105.926066, 106.179867, 54.445933, 28.3384, 14.602233, 8.1173667, 4.892267])
serial_runtime = 60.7673333


plt.rcParams.update({
    "font.family": "serif",
    "font.size": 14,
    "axes.labelsize": 16,
    "axes.titlesize": 18,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "legend.fontsize": 13,
    "figure.dpi": 120
})

fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(processes, parallel_runtimes, marker='o', linestyle='-', linewidth=2,
        color='steelblue', label='Parallel Runtime')

ax.axhline(serial_runtime, color='gray', linestyle='--', linewidth=1.5,
           label=f'Serial Runtime ({serial_runtime:.1f}s)')

ax.set_title("Runtime vs. Number of Processes (4096 x 4096 Grid)")
ax.set_xlabel("Number of Processes")
ax.set_ylabel("Runtime (seconds)")

ax.set_xticks(processes)
ax.get_xaxis().set_major_formatter(ScalarFormatter())
ax.grid(True, which='major', linestyle=':', linewidth=0.8, alpha=0.6)

# for x, y in zip(processes, parallel_runtimes):
#     ax.annotate(f"{y:.1f}s", (x, y), textcoords="offset points",
#                 xytext=(0, 8), ha='center', fontsize=11)

ax.legend(frameon=True, loc='upper right', bbox_to_anchor=(1, 0.92))

plt.tight_layout()
plt.show()
