import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter


# ASYNC OPTIMIZATION (ONLY) OUTPUT
# Format: {[processes]: [runtimes]}
async_only_runtimes = {
    1: [33.193093, 33.584682, 32.897391],
    2: [32.932571, 33.104590, 32.868242],
    4: [32.196433, 32.196755, 32.162884],
    8: [18.718433, 20.014369, 24.154047],
    16: [31.941998, 31.039288, 32.082699],
    32: [32.303755, 32.154515, 32.215367],
    64: [32.158465, 32.147540, 32.303304]
}
base_mpi_runtimes = {
    1: [38.331253, 38.262337, 38.502779],
    2: [47.212411, 46.860444, 46.984581],
    4: [32.256538, 32.204685, 32.228431],
    8: [32.033573, 32.122912, 32.182895],
    16: [32.259175, 32.014739, 31.421131],
    32: [32.066184, 31.958959, 28.790180],
    64: [32.136130, 31.523680, 31.837995]
}
# Using the same serial time from before -- as this is basically the same programme still
serial_runtime = np.mean([32.308677, 32.251042, 32.508082])


# Async + OMP Runtimes
async_omp_runtimes = {
    1: [8.097727, 8.091827, 8.090564],
    2: [4.704039, 4.899853, 4.683437],
    4: [2.247665, 2.262453, 2.249726],
    8: [1.069484, 1.872519, 1.142267],
    16: [2.234144, 1.842109, 1.858833],
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

def get_base_mpi_means():
    return [np.average(curr_runtime) for curr_runtime in [base_mpi_runtimes[process] for process in sorted(list(base_mpi_runtimes.keys()))]]
    # process_count = list(base_mpi_runtimes.keys())
    # mean_runtime, std_dev, min_time, max_time = []
    # print("###### STATS FOR STRONG-SCALING RUNTIMES ######")

    # for process in sorted(process_count):
    #     curr_runtimes = strong_parallel_runtimes[process]
    #     curr_mean, curr_std, curr_min, curr_max = np.average(curr_runtimes), np.std(curr_runtimes), min(curr_runtimes), max(curr_runtimes)
    #     print(f"#### For {process} processes ####")
    #     print(f"All Times: {curr_runtimes}\nMean Runtime: {curr_mean}\nStd Dev: {curr_std}\nMin Observation: {curr_min}\nMax Observation: {curr_max}")
    #     mean_runtime.append(curr_mean)
    #     std_dev.append(curr_std)
    #     min_time.append(curr_min)
    #     max_time.append(curr_max)    

def get_stats_from_dict(data_dict, data_dict_name):
    process_count = list(data_dict.keys())
    mean_runtime, std_dev, min_time, max_time = [], [], [], []
    print(f"###### STATS FOR {data_dict_name} RUNTIMES ######")

    for process in sorted(process_count):
        curr_runtimes = data_dict[process]
        curr_mean, curr_std, curr_min, curr_max = np.average(curr_runtimes), np.std(curr_runtimes), min(curr_runtimes), max(curr_runtimes)
        print(f"#### For {process} processes ####")
        print(f"All Times: {curr_runtimes}\nMean Runtime: {curr_mean}\nStd Dev: {curr_std}\nMin Observation: {curr_min}\nMax Observation: {curr_max}")
        mean_runtime.append(curr_mean)
        std_dev.append(curr_std)
        min_time.append(curr_min)
        max_time.append(curr_max)
    
    return mean_runtime, std_dev, min_time, max_time

def base_mpi_vs_async_mpi():
    base_mpi_means = get_base_mpi_means()
    mean_runtime, _, _, _ = get_stats_from_dict(async_only_runtimes, "ASYNC-ONLY")

    process_count = list(async_only_runtimes.keys())

    # TODO: Maybe add plot lines for std deviation/error? 
    ax.plot(process_count, base_mpi_means, marker='o', linestyle='-', linewidth=2,
            color='steelblue', label='Base MPI Runtime')
    ax.plot(process_count, mean_runtime, marker="x", linestyle="-", linewidth=2, color="red", label="Async (Non-Blocking Opt.) MPI")

    ax.set_title(f"Base MPI vs Async MPI Optimization (6.4mil elements, 1k iterations)")
    ax.set_xlabel("Number of Processes")
    ax.set_ylabel("Runtime (seconds)")

    ax.set_xticks(process_count)
    ax.get_xaxis().set_major_formatter(ScalarFormatter())
    ax.grid(True, which='major', linestyle=':', linewidth=0.8, alpha=0.6)

    # for x, y in zip(process_count, mean_runtime):
    #     ax.annotate(f"{y:.1f}s", (x, y), textcoords="offset points",
    #                 xytext=(0, 8), ha='center', fontsize=11)

    ax.legend(frameon=True, loc='upper right', bbox_to_anchor=(1, 0.92))

    plt.tight_layout()
    plt.show()

def base_mpi_vs_async_omp_mpi():
    base_mpi_runtimes = get_base_mpi_means()
    # We only go up to 16 processes for the omp runtimes on multiple machines
    # So, don't care about the last 2 mpi runtimes
    base_mpi_runtimes = base_mpi_runtimes[:len(base_mpi_runtimes)-2]
    mean_runtime, _, _, _ = get_stats_from_dict(async_omp_runtimes, "ASYNC + OMP")
    process_count = list(async_omp_runtimes.keys())

    # TODO: Maybe add plot lines for std deviation/error? 
    ax.plot(process_count, base_mpi_runtimes, marker='o', linestyle='-', linewidth=2,
            color='steelblue', label='Base MPI Runtime')
    ax.plot(process_count, mean_runtime, marker="x", linestyle="-", linewidth=2, color="purple", label="Async MPI + OMP (8 Threads/process)")

    ax.set_title(f"Async MPI + OMP Opt. on up-to 4 Nodes")
    ax.set_xlabel("Number of Processes")
    ax.set_ylabel("Runtime (seconds)")

    ax.set_xticks(process_count)
    ax.get_xaxis().set_major_formatter(ScalarFormatter())
    ax.grid(True, which='major', linestyle=':', linewidth=0.8, alpha=0.6)

    # for x, y in zip(process_count, mean_runtime):
    #     ax.annotate(f"{y:.1f}s", (x, y), textcoords="offset points",
    #                 xytext=(0, 8), ha='center', fontsize=11)

    ax.legend(frameon=True, loc='upper right', bbox_to_anchor=(1, 0.92))

    plt.tight_layout()
    plt.show()

def plot_everything():
    base_mpi_runtimes = get_base_mpi_means()
    # We only go up to 16 processes for the omp runtimes on multiple machines
    # So, don't care about the last 2 mpi runtimes
    base_mpi_runtimes = base_mpi_runtimes[:len(base_mpi_runtimes)-2]
    mean_runtime_async_omp, _, _, _ = get_stats_from_dict(async_omp_runtimes, "ASYNC + OMP")
    # Again, only care about up-to 16 processes for the async-only optimization
    mean_runtime_async, _, _, _ = get_stats_from_dict(async_only_runtimes, "ASYNC-ONLY")
    mean_runtime_async = mean_runtime_async[:len(mean_runtime_async)-2]
    process_count = list(async_omp_runtimes.keys())

    # TODO: Maybe add plot lines for std deviation/error? 
    ax.plot(process_count, base_mpi_runtimes, marker='o', linestyle='-', linewidth=2,
            color='steelblue', label='Base MPI')
    ax.plot(process_count, mean_runtime_async, marker="^", linestyle="-", linewidth=2, color="red", label="Async MPI (Opt 1)")
    ax.plot(process_count, mean_runtime_async_omp, marker="x", linestyle="-", linewidth=2, color="purple", label="Async MPI + OMP (Opt 2)")
    

    ax.set_title(f"Base MPI vs Both Optimizations")
    ax.set_xlabel("Number of Processes")
    ax.set_ylabel("Runtime (seconds)")

    ax.set_xticks(process_count)
    ax.get_xaxis().set_major_formatter(ScalarFormatter())
    ax.grid(True, which='major', linestyle=':', linewidth=0.8, alpha=0.6)

    # for x, y in zip(process_count, mean_runtime):
    #     ax.annotate(f"{y:.1f}s", (x, y), textcoords="offset points",
    #                 xytext=(0, 8), ha='center', fontsize=11)

    ax.legend(frameon=True, loc='upper right', bbox_to_anchor=(1, 0.92))

    plt.tight_layout()
    plt.show()

# Base MPI vs Async MPI
# base_mpi_vs_async_mpi()
# Base MPI vs Async + OMP MPI across 4 Nodes
# base_mpi_vs_async_omp_mpi()
# Plot of Base and both optimizations
plot_everything()


