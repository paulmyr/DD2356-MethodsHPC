THREAD_COUNTS = [1, 2, 4, 8, 16, 20, 24, 28, 32, 64, 128]
SERIAL_RUNTIME = [0.332] * len(THREAD_COUNTS)
OMP_OUTPUT = [0.325, 0.578, 0.505, 0.455, 0.423, 0.571, 0.635, 0.508, 0.876, 0.834, 0.745]
OMP_LOCAL_OUTPUT = [0.326, 0.539, 0.512, 0.249, 0.222, 0.201, 0.184, 0.155, 0.140, 0.060, 0.047]
OMP_LOCAL_NO_SHARING_OUTPUT = [0.325, 0.163, 0.082, 0.041, 0.021, 0.028, 0.024, 0.026, 0.022, 0.022, 0.025]
OMP_CRITICAL_OUTPUT = [1.105, 2.155, 3.373, 4.911, 6.708, 7.191, 7.712, 8.152, 8.600, 10.508, 9.550]

import matplotlib.pyplot as plt

plt.style.use('seaborn-v0_8-muted') 

fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(THREAD_COUNTS, SERIAL_RUNTIME, label='Serial', marker='o', linestyle='-', color='#1f77b4', linewidth=2)
ax.plot(THREAD_COUNTS, OMP_OUTPUT, label='Vanilla OMP', marker='s', linestyle='--', color='#ff7f0e', linewidth=2)
ax.plot(THREAD_COUNTS, OMP_LOCAL_OUTPUT, label='OMP w/ Local Sum', marker='^', linestyle=':', color='#2ca02c', linewidth=2)
ax.plot(THREAD_COUNTS, OMP_LOCAL_NO_SHARING_OUTPUT, label='OMP w/ Local Sum (no sharing)', marker='d', linestyle='-.', color='#9467bd', linewidth=2)
# ax.plot(THREAD_COUNTS, OMP_CRITICAL_OUTPUT, label="OMP w/ Critical Region", marker='p', linestyle='-', color='#8c564b', linewidth=2)

ax.set_xlabel("Number of Threads", fontsize=14, fontweight='bold', color='darkblue')
ax.set_ylabel("Runtime (seconds)", fontsize=14, fontweight='bold', color='darkblue')
ax.set_title("Comparison of Serial and OMP Summation Runtimes", fontsize=16, fontweight='bold')

ax.grid(True, which="both", linestyle='--', alpha=0.7)
ax.tick_params(axis='both', labelsize=12, width=1.2)

# Uncomment this to have legend inside the box
# ax.legend(loc='upper right', fontsize=12, frameon=False)

# Uncomment this to have the legend outside the box
ax.legend(loc='upper left', fontsize=12, frameon=False, bbox_to_anchor=(1.05, 1))

plt.tight_layout()

plt.show()
