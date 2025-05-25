import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter


# ASYNC OPTIMIZATION (ONLY) OUTPUT
# Format: {[processes]: [runtimes]}
async_only_runtimes = {
    1: [33.314620, 33.274368, 33.134775],
    2: [32.657642, 32.946989, 32.688454],
    4: [32.161904, 32.177045, 32.185109],
    8: [22.457152, 22.628679, 27.692717],
    16: [32.197147, 32.283180, 32.234864],
    32: [32.027466, 32.313937, 32.367093],
    64: [32.407803, 32.237467, 32.339952]
}
base_mpi_runtimes = {
    1: [39.623333, 39.043362, 38.190578],
    2: [46.848599, 46.924505, 47.156570],
    4: [32.265520, 32.296422, 32.261580],
    8: [32.051071, 32.208476, 31.030969],
    16: [31.999440, 32.186232, 31.639870],
    32: [32.122833, 32.077514, 32.261366],
    64: [32.360444, 32.286459, 32.287953]
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


# Comparing Blocking MPI with Async-Only Optimization on Different grid sizes (8 processes)
# Format: {[grid_Size]: [...runtimes...]}
base_mpi_8_cores = {
    640: [19.440205, 12.955923, 14.383932],
    6_400: [28.300037, 18.435593, 32.151603],
    64_000: [20.864851, 29.856810, 31.744920],
    640_000: [31.670828, 32.022360, 20.465776],
    6_400_000: [32.082041, 29.775050, 31.380977]
}

async_only_8_cores = {
    640: [14.595929, 15.859917, 18.208223],
    6_400: [25.968355, 30.064053, 31.920065],
    64_000: [31.348323, 21.944452, 18.804577],
    640_000: [21.514960, 12.852325, 25.965568],
    6_400_000: [15.195069, 23.422439, 17.351784]
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

def compare_base_async_only_8_process():
    mean_runtime_base_8, _, _, _ = get_stats_from_dict(base_mpi_8_cores, "Base MPI (8 Cores)")
    mean_runtime_async_8, _, _, _ = get_stats_from_dict(async_only_8_cores, "Async Only (8 Cores)")

    grid_sizes = list(base_mpi_8_cores.keys())

    ax.plot(grid_sizes, mean_runtime_base_8, marker="^", linestyle="-", linewidth=2, color="red", label="Base MPI")
    ax.plot(grid_sizes, mean_runtime_async_8, marker="x", linestyle="-", linewidth=2, color="purple", label="Async MPI")

    ax.set_title(f"Base MPI vs Async MPI (8 Processes, 1 Node)")
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

# # Base MPI vs Async MPI
# base_mpi_vs_async_mpi()
# # Base MPI vs Async + OMP MPI across 4 Nodes
# base_mpi_vs_async_omp_mpi()
# # Plot of Base and both optimizations
# plot_everything()
# # Comparison of Base and Async MPI on different grid sizes
# compare_base_async_only_8_process()


