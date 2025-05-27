import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter


# Strong Scaling Times
strong_parallel_runtimes = {
    1: [44.945557, 44.879691, 44.903810],
    2: [22.672265, 22.753485, 22.737768],
    4: [11.516030, 11.496270, 11.496318],
    8: [5.667573, 5.685608, 5.672346],
    16: [2.860172, 2.855245, 2.863610],
    32: [1.444306, 1.445751, 1.451835],
    64: [0.758845, 0.750487, 0.752842],
    128: [0.464932, 0.455544, 0.456503],
    256: [0.475227, 0.473653, 0.475763]
}
serial_runtime = np.mean([32.266016, 32.375750, 32.089423])



# Weak Scaling Times
weak_parallel_runtimes = {
    1: [0.696535, 0.697438, 0.698123],
    2: [0.709091, 0.718187, 0.710930],
    4: [0.725008, 0.724247, 0.716528],
    8: [0.725760, 0.720584, 0.725570],
    16: [0.733580, 0.734949, 0.731773],
    32: [0.736842, 0.748247, 0.739362],
    64: [0.755325, 0.753304, 0.748040],
    128: [0.880054, 0.884189, 0.887827],
    256: [1.715259, 1.701976, 1.694138]
}

# OpenMP GPU Handoff
gpu_grid_runtimes = {
    640: [0.702867, 0.346366, 0.345958],
    6400: [0.371401, 0.372639, 0.376987],
    64_000: [0.641372, 0.647557, 0.641322],
    640_000: [2.544907, 2.541085, 2.554037],
    6_400_000: [21.204373, 20.643135, 20.640450]
}

serial_grid_runtimes = {
    640: [0.003045, 0.003095, 0.003043],
    6400: [0.030393, 0.030523, 0.030454],
    64_000: [0.305961, 0.304280, 0.347505],
    640_000: [3.115291, 3.080597, 3.075924],
    6_400_000: [32.266016, 32.375750, 32.089423]
}

# OMP Runtimes with 128 threads
omp_grid_runtimes = {
    640: [0.032708, 0.040456, 0.037860],
    6400: [0.039851, 0.040001, 0.037752],
    64_000: [0.043264, 0.049828, 0.043330],
    640_000: [0.124054, 0.122537, 0.122379],
    6_400_000: [0.852577, 0.850906, 0.848543]
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

def get_stats_from_dict(data_dict, data_dict_name, entity="processes"):
    entity_count = list(data_dict.keys())
    mean_runtime, std_dev, min_time, max_time = [], [], [], []
    print(f"###### STATS FOR {data_dict_name} RUNTIMES ######")

    for curr_entity in sorted(entity_count):
        curr_runtimes = data_dict[curr_entity]
        curr_mean, curr_std, curr_min, curr_max = np.average(curr_runtimes), np.std(curr_runtimes), min(curr_runtimes), max(curr_runtimes)
        print(f"#### For {curr_entity} {entity} ####")
        print(f"All Times: {curr_runtimes}\nMean Runtime: {curr_mean}\nStd Dev: {curr_std}\nMin Observation: {curr_min}\nMax Observation: {curr_max}")
        mean_runtime.append(curr_mean)
        std_dev.append(curr_std)
        min_time.append(curr_min)
        max_time.append(curr_max)
        print("\n---------------------\n")
    
    return mean_runtime, std_dev, min_time, max_time


def plot_serial_parallel_comparison(title, show_serial=True):
    process_count = list(strong_parallel_runtimes.keys())
    mean_runtime, std_dev, min_time, max_time = [], [], [], []
    print("###### STATS FOR STRONG-SCALING RUNTIMES ######")

    for process in sorted(process_count):
        curr_runtimes = strong_parallel_runtimes[process]
        curr_mean, curr_std, curr_min, curr_max = np.average(curr_runtimes), np.std(curr_runtimes), min(curr_runtimes), max(curr_runtimes)
        print(f"#### For {process} threads ####")
        print(f"All Times: {curr_runtimes}\nMean Runtime: {curr_mean}\nStd Dev: {curr_std}\nMin Observation: {curr_min}\nMax Observation: {curr_max}")
        mean_runtime.append(curr_mean)
        std_dev.append(curr_std)
        min_time.append(curr_min)
        max_time.append(curr_max)
        print("\n---------------------\n")

    # TODO: Maybe add plot lines for std deviation/error? 
    ax.plot(process_count, mean_runtime, marker='o', linestyle='-', linewidth=2,
            color='steelblue', label='OMP Runtime')

    if show_serial:
        ax.axhline(serial_runtime, color='gray', linestyle='--', linewidth=1.5,
                label=f'Serial Runtime ({serial_runtime:.1f}s)')

    ax.set_title(f"{title} (6.4mil elements, 1k iterations)")
    ax.set_xlabel("Number of Threads (Log Scale)")
    ax.set_ylabel("Runtime (seconds)")

    ax.set_xticks(process_count)
    ax.get_xaxis().set_major_formatter(ScalarFormatter())
    ax.grid(True, which='major', linestyle=':', linewidth=0.8, alpha=0.6)

    for x, y in zip(process_count, mean_runtime):
        ax.annotate(f"{y:.1f}s", (x, y), textcoords="offset points",
                    xytext=(0, 8), ha='center', fontsize=11)

    ax.legend(frameon=True, loc='upper right', bbox_to_anchor=(1, 0.92))

    plt.tight_layout()
    plt.xscale("log")
    plt.show()

def plot_weak_scaling():
    process_count = list(weak_parallel_runtimes.keys())
    mean_runtime, std_dev, min_time, max_time = [], [], [], []
    print("###### STATS FOR WEAK-SCALING RUNTIMES (100k items per threads, 1k iterations) ######")

    for process in sorted(process_count):
        curr_runtimes = weak_parallel_runtimes[process]
        curr_mean, curr_std, curr_min, curr_max = np.average(curr_runtimes), np.std(curr_runtimes), min(curr_runtimes), max(curr_runtimes)
        print(f"#### For {process} threads ####")
        print(f"All Times: {curr_runtimes}\nMean Runtime: {curr_mean}\nStd Dev: {curr_std}\nMin Observation: {curr_min}\nMax Observation: {curr_max}")
        mean_runtime.append(curr_mean)
        std_dev.append(curr_std)
        min_time.append(curr_min)
        max_time.append(curr_max)
        print("\n---------------------\n")

    # TODO: Maybe add plot lines for std deviation/error? 
    ax.plot(process_count, mean_runtime, marker='o', linestyle='-', linewidth=2,
            color='steelblue', label='OMP Runtime')

    ax.set_title(f"Weak Scaling Plot (100k/per thread, 1k iters)")
    ax.set_xlabel("Number of Threads (Log Scale)")
    ax.set_ylabel("Runtime (seconds)")

    # ax.set_yticks(range(0, 50, 5))
    ax.set_xticks(process_count)
    ax.get_xaxis().set_major_formatter(ScalarFormatter())
    ax.grid(True, which='major', linestyle=':', linewidth=0.8, alpha=0.6)

    # for x, y in zip(process_count, mean_runtime):
    #     ax.annotate(f"{y:.1f}s", (x, y), textcoords="offset points",
    #                 xytext=(0, 8), ha='center', fontsize=11)

    ax.legend(frameon=True, loc='upper right', bbox_to_anchor=(1, 0.92))

    plt.tight_layout()
    plt.xscale("log")
    plt.show()

def compare_gpu_serial():
    mean_runtime_gpu, _, _, _ = get_stats_from_dict(gpu_grid_runtimes, "GPU Runtime", entity="elements")
    mean_runtime_serial, _, _, _ = get_stats_from_dict(serial_grid_runtimes, "Serial Runtime", entity="elements")

    grid_sizes = list(gpu_grid_runtimes.keys())

    ax.plot(grid_sizes, mean_runtime_gpu, marker="^", linestyle="-", linewidth=2, color="red", label="GPU Runtime")
    ax.plot(grid_sizes, mean_runtime_serial, marker="x", linestyle="-", linewidth=2, color="purple", label="Serial Runtime")

    ax.set_title(f"OpenMP GPU Hand-off vs Serial Runtime")
    ax.set_xlabel("Grid Size (Log Scale)")
    ax.set_ylabel("Runtime (seconds)")

    ax.set_xticks(grid_sizes)
    ax.get_xaxis().set_major_formatter(ScalarFormatter())
    ax.grid(True, which='major', linestyle=':', linewidth=0.8, alpha=0.6)

    # for x, y in zip(process_count, mean_runtime):
    #     ax.annotate(f"{y:.1f}s", (x, y), textcoords="offset points",
    #                 xytext=(0, 8), ha='center', fontsize=11)

    ax.legend(frameon=True, loc='upper right', bbox_to_anchor=(1, 0.92))

    plt.tight_layout()
    plt.xscale("log")
    plt.show()

# # Strong Scaling Plot (With Serial Comparison)
plot_serial_parallel_comparison(title="Strong Scaling Plot", show_serial=True)

# # Weak Scaling Plot
# plot_weak_scaling()

# Grid Size Comparison for GPU
# compare_gpu_serial()

# get_stats_from_dict(omp_grid_runtimes, "OpenMP (128 Threads)", "threads")
get_stats_from_dict(gpu_grid_runtimes, "GPU Runtime", entity="elements")