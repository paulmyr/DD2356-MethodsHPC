import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter

# GENERAL PURPOSE ARRAYS
processes = np.array([1, 2, 4, 8, 16, 32, 64])

# STRONG SCALING OUTPUT (grid_size: 64k)
strong_parallel_runtimes = np.array([2.286553, 182.384184, 194.5907123, 217.889325333, 273.67067133, 329.56532066667, 361.425328])
strong_serial_runtime = 2.2942683333333

# WEAK SCALING OUTPUT 
weak_parallel_runtimes = np.array([0.0323533, 182.778657, 216.88798, 253.73465, 250.102656, 348.02532, 336.28399])

# NODE COUNT OUTPUT
node_counts = np.array([1, 2, 4, 8, 16])
node_counts_runtime = np.array([329.56532066667, 385.51837966667, 347.413121, 356.071311, 332.15855]) 

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

def plot_serial_parallel_comparison():
    ax.plot(processes, strong_parallel_runtimes, marker='o', linestyle='-', linewidth=2,
            color='steelblue', label='MPI Runtime')

    # ax.axhline(strong_serial_runtime, color='gray', linestyle='--', linewidth=1.5,
    #         label=f'Serial Runtime ({strong_serial_runtime:.1f}s)')

    ax.set_title("Strong Scaling Plot (64000 elements)")
    ax.set_xlabel("Number of Processes")
    ax.set_ylabel("Runtime (seconds)")

    ax.set_xticks(processes)
    ax.get_xaxis().set_major_formatter(ScalarFormatter())
    ax.grid(True, which='major', linestyle=':', linewidth=0.8, alpha=0.6)

    for x, y in zip(processes, strong_parallel_runtimes):
        ax.annotate(f"{y:.1f}s", (x, y), textcoords="offset points",
                    xytext=(0, 8), ha='center', fontsize=11)

    ax.legend(frameon=True, loc='upper right', bbox_to_anchor=(1, 0.92))

    plt.tight_layout()
    plt.show()

def plot_weak_scaling():
    ax.plot(processes, weak_parallel_runtimes, marker='o', linestyle='-', linewidth=2,
            color='steelblue', label="MPI Runtime")

    ax.set_title("Weak Scaling Plot (Each Process: 1000 items, 5000 iterations)")
    ax.set_xlabel("Number of Processes")
    ax.set_ylabel("Runtime (seconds)")

    ax.set_xticks(processes)
    ax.get_xaxis().set_major_formatter(ScalarFormatter())
    ax.grid(True, which='major', linestyle=':', linewidth=0.8, alpha=0.6)

    for x, y in zip(processes, weak_parallel_runtimes):
        ax.annotate(f"{y:.1f}s", (x, y), textcoords="offset points",
                    xytext=(0, 8), ha='center', fontsize=11)

    ax.legend(frameon=True, loc='upper right', bbox_to_anchor=(1, 0.92))

    plt.tight_layout()
    plt.show()

def plot_diff_node_counts():
    ax.plot(node_counts, node_counts_runtime, marker='o', linestyle='-', linewidth=2,
            color='steelblue', label="MPI Runtime")

    ax.set_title("Runtime for Different Node Counts (32 Processes, Distributed Equally)")
    ax.set_xlabel("Number of Nodes")
    ax.set_ylabel("Runtime (seconds)")

    ax.set_yticks(range(200, 500, 50))
    ax.set_xticks(node_counts)
    ax.get_xaxis().set_major_formatter(ScalarFormatter())
    ax.grid(True, which='major', linestyle=':', linewidth=0.8, alpha=0.6)

    for x, y in zip(node_counts, node_counts_runtime):
        ax.annotate(f"{y:.1f}s", (x, y), textcoords="offset points",
                    xytext=(0, 8), ha='center', fontsize=11)

    ax.legend(frameon=True, loc='upper right', bbox_to_anchor=(1, 0.92))

    plt.tight_layout()
    plt.show()

plot_serial_parallel_comparison()
