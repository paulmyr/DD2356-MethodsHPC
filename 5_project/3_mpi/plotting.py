import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter


# STRONG SCALING OUTPUT (grid_size: 6.4mil)
# Format: {[processes]: [runtimes]}
strong_parallel_runtimes = {
    1: [40.087363, 39.939055, 39.717535],
    2: [47.084920, 47.210627, 47.146134],
    4: [31.512342, 31.336741, 31.585777],
    8: [31.441525, 32.050834, 32.176548],
    16: [31.983243, 32.220439, 32.248081],
    32: [32.318019, 32.293924, 31.945332],
    64: [32.317748, 32.369135, 32.381524]
}
serial_runtime = np.mean([32.254506, 32.225373, 32.356388])

# WEAK SCALING OUTPUT
# 100000 elements per process
weak_parallel_runtimes = {
    1: [0.613438, 0.570855, 0.646987],
    2: [31.745043, 31.677046, 31.465048],
    4: [32.134006, 32.053827, 32.061349],
    8: [28.507372, 30.451733, 29.126295],
    16: [31.609730, 32.033280, 30.328886],
    32: [32.345151, 32.206800, 32.161842],
    64: [32.301573, 32.290829, 32.298101]
}


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
    process_count = list(strong_parallel_runtimes.keys())
    mean_runtime, std_dev, min_time, max_time = [], [], [], []
    print("###### STATS FOR STRONG-SCALING RUNTIMES ######")

    for process in sorted(process_count):
        curr_runtimes = strong_parallel_runtimes[process]
        curr_mean, curr_std, curr_min, curr_max = np.average(curr_runtimes), np.std(curr_runtimes), min(curr_runtimes), max(curr_runtimes)
        print(f"#### For {process} processes ####")
        print(f"All Times: {curr_runtimes}\nMean Runtime: {curr_mean}\nStd Dev: {curr_std}\nMin Observation: {curr_min}\nMax Observation: {curr_max}")
        mean_runtime.append(curr_mean)
        std_dev.append(curr_std)
        min_time.append(curr_min)
        max_time.append(curr_max)

    # TODO: Maybe add plot lines for std deviation/error? 
    ax.plot(process_count, mean_runtime, marker='o', linestyle='-', linewidth=2,
            color='steelblue', label='MPI Runtime')

    if show_serial:
        ax.axhline(serial_runtime, color='gray', linestyle='--', linewidth=1.5,
                label=f'Serial Runtime ({serial_runtime:.1f}s)')

    ax.set_title(f"{title} (6.4mil elements, 1k iterations)")
    ax.set_xlabel("Number of Processes")
    ax.set_ylabel("Runtime (seconds)")

    ax.set_xticks(process_count)
    ax.get_xaxis().set_major_formatter(ScalarFormatter())
    ax.grid(True, which='major', linestyle=':', linewidth=0.8, alpha=0.6)

    for x, y in zip(process_count, mean_runtime):
        ax.annotate(f"{y:.1f}s", (x, y), textcoords="offset points",
                    xytext=(0, 8), ha='center', fontsize=11)

    ax.legend(frameon=True, loc='upper right', bbox_to_anchor=(1, 0.92))

    plt.tight_layout()
    plt.show()

def plot_weak_scaling():
    process_count = list(weak_parallel_runtimes.keys())
    mean_runtime, std_dev, min_time, max_time = [], [], [], []
    print("###### STATS FOR WEAK-SCALING RUNTIMES (100k items per process, 1k iterations) ######")

    for process in sorted(process_count):
        curr_runtimes = weak_parallel_runtimes[process]
        curr_mean, curr_std, curr_min, curr_max = np.average(curr_runtimes), np.std(curr_runtimes), min(curr_runtimes), max(curr_runtimes)
        print(f"#### For {process} processes ####")
        print(f"All Times: {curr_runtimes}\nMean Runtime: {curr_mean}\nStd Dev: {curr_std}\nMin Observation: {curr_min}\nMax Observation: {curr_max}")
        mean_runtime.append(curr_mean)
        std_dev.append(curr_std)
        min_time.append(curr_min)
        max_time.append(curr_max)

    # TODO: Maybe add plot lines for std deviation/error? 
    ax.plot(process_count, mean_runtime, marker='o', linestyle='-', linewidth=2,
            color='steelblue', label='MPI Runtime')

    ax.set_title(f"Weak Scaling Plot (100k/per process, 1k iters)")
    ax.set_xlabel("Number of Processes")
    ax.set_ylabel("Runtime (seconds)")

    ax.set_yticks(range(0, 50, 5))
    ax.set_xticks(process_count)
    ax.get_xaxis().set_major_formatter(ScalarFormatter())
    ax.grid(True, which='major', linestyle=':', linewidth=0.8, alpha=0.6)

    # for x, y in zip(process_count, mean_runtime):
    #     ax.annotate(f"{y:.1f}s", (x, y), textcoords="offset points",
    #                 xytext=(0, 8), ha='center', fontsize=11)

    ax.legend(frameon=True, loc='upper right', bbox_to_anchor=(1, 0.92))

    plt.tight_layout()
    plt.show()


# Strong Scaling
# plot_serial_parallel_comparison(title="Strong Scaling Plot", show_serial=True)
# Weak Scaling
plot_weak_scaling()

