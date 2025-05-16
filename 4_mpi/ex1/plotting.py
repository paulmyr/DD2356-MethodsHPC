import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter

# GENERAL PURPOSE ARRAYS
processes = np.array([1, 2, 4, 8, 16, 32, 64])

# STRONG SCALING OUTPUT (grid_size: 6.4mil)
strong_parallel_runtimes = np.array([206.444177, 318.124553, 144.3341293, 159.665902, 157.655496, 160.07411533, 159.912872])
strong_serial_runtime = 211.29658366667

# WEAK SCALING OUTPUT 
weak_parallel_runtimes = np.array([3.246998, 159.559421, 107.02601166, 99.09132867, 128.22297466, 154.52977467, 160.066075333])

# NODE COUNT OUTPUT
node_counts = np.array([1, 2, 4, 8])
node_counts_runtime = np.array([160.07411533, 157.285153, 149.94199833333, 156.138331]) 

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

def plot_serial_parallel_comparison(title, show_serial=True):
    ax.plot(processes, strong_parallel_runtimes, marker='o', linestyle='-', linewidth=2,
            color='steelblue', label='MPI Runtime')

    if show_serial:
        ax.axhline(strong_serial_runtime, color='gray', linestyle='--', linewidth=1.5,
                label=f'Serial Runtime ({strong_serial_runtime:.1f}s)')

    ax.set_title(f"{title} (6.4mil elements, 5k iterations)")
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

    ax.set_title("Weak Scaling Plot (Each Process: 100k items, 5k iterations)")
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
    
    ax.axhline(strong_serial_runtime, color='gray', linestyle='--', linewidth=1.5,
            label=f'Serial Runtime ({strong_serial_runtime:.1f}s)')

    ax.set_title("Runtime for Different Node Counts (32 Processes, Distributed Equally)")
    ax.set_xlabel("Number of Nodes")
    ax.set_ylabel("Runtime (seconds)")

    ax.set_yticks(range(100, 300, 50))
    ax.set_xticks(node_counts)
    ax.get_xaxis().set_major_formatter(ScalarFormatter())
    ax.grid(True, which='major', linestyle=':', linewidth=0.8, alpha=0.6)

    for x, y in zip(node_counts, node_counts_runtime):
        ax.annotate(f"{y:.1f}s", (x, y), textcoords="offset points",
                    xytext=(0, 8), ha='center', fontsize=11)

    ax.legend(frameon=True, loc='upper right', bbox_to_anchor=(1, 0.92))

    plt.tight_layout()
    plt.show()

# MPI vs Serial Comparison
# plot_serial_parallel_comparison(title="Serial vs MPI")
# Strong Scaling
# plot_serial_parallel_comparison(title="Strong Scaling", show_serial=False)
# Weak Scaling
plot_weak_scaling()
# Different Nodes Plot
# plot_diff_node_counts()

