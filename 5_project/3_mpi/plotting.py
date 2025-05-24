import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter


# STRONG SCALING OUTPUT (grid_size: 6.4mil)
# Format: {[processes]: [runtimes]}
strong_parallel_runtimes = {
    1: [38.331253, 38.262337, 38.502779],
    2: [47.212411, 46.860444, 46.984581],
    4: [32.256538, 32.204685, 32.228431],
    8: [32.033573, 32.122912, 32.182895],
    16: [32.259175, 32.014739, 31.421131],
    32: [32.066184, 31.958959, 28.790180],
    64: [32.136130, 31.523680, 31.837995]
}
serial_runtime = np.mean([32.308677, 32.251042, 32.508082])

# WEAK SCALING OUTPUT
# 100000 elements per process
weak_parallel_runtimes = {
    1: [0.690983, 0.586776, 0.592322],
    2: [31.995929, 31.985169, 31.877182],
    4: [31.997560, 32.085427, 32.070640],
    8: [19.956081, 18.290667, 18.853176],
    16: [29.637531, 20.923783, 29.798923],
    32: [30.764566, 31.855628, 30.468660],
    64: [31.696626, 32.155175, 32.234525]
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

# 640 6400 64000 640000 6400000

