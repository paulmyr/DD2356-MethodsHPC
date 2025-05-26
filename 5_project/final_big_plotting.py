import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter

serial_runtimes = {
    640: [0.003045, 0.003095, 0.003043],
    6400: [0.030393, 0.030523, 0.030454],
    64_000: [0.305961, 0.304280, 0.347505],
    640_000: [3.115291, 3.080597, 3.075924],
    6_400_000: [32.266016, 32.375750, 32.089423]
}

# OMP Runtimes with 128 threads
omp_runtimes = {
    640: [0.032708, 0.040456, 0.037860],
    6400: [0.039851, 0.040001, 0.037752],
    64_000: [0.043264, 0.049828, 0.043330],
    640_000: [0.124054, 0.122537, 0.122379],
    6_400_000: [0.852577, 0.850906, 0.848543]
}

# gpu runtimes
gpu_runtimes = {
    640: [0.702867, 0.346366, 0.345958],
    6400: [0.371401, 0.372639, 0.376987],
    64_000: [0.641372, 0.647557, 0.641322],
    640_000: [2.544907, 2.541085, 2.554037],
    6_400_000: [21.204373, 20.643135, 20.640450]  
}

# TODO: CHANGE THIS, THIS IS FOR ONLY 8 PROCESSES ATM AS A STAND-IN
mpi_runtime = {
    640: [19.440205, 12.955923, 14.383932],
    6_400: [28.300037, 18.435593, 32.151603],
    64_000: [20.864851, 29.856810, 31.744920],
    640_000: [31.670828, 32.022360, 20.465776],
    6_400_000: [32.082041, 29.775050, 31.380977]
}

# Runtime of async MPI optimization (8 processes)
async_mpi_runtime = {
    640: [14.595929, 15.859917, 18.208223],
    6_400: [25.968355, 30.064053, 31.920065],
    64_000: [31.348323, 21.944452, 18.804577],
    640_000: [21.514960, 12.852325, 25.965568],
    6_400_000: [15.195069, 23.422439, 17.351784]
}

# Runtime of async MPI (16 processes) + OpenMP (16 threads) across 4 nodes
async_omp_mpi_runtime = {
    640: [0.092310, 0.049394, 0.063659],
    6400: [0.052928, 0.056507, 0.062249],
    64_000: [0.072029, 0.064318, 0.060017],
    640_000: [0.110865, 0.113847, 0.102050],
    6_400_000: [0.477182, 0.499364, 0.497117]
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

def plot_stuff():
    serial, _, _, _ = get_stats_from_dict(serial_runtimes, "SERIAL IMPL")
    openmp, _, _, _ = get_stats_from_dict(omp_runtimes, "OpenMP IMPL")
    gpu, _, _, _ = get_stats_from_dict(gpu_runtimes, "OpenMP GPU Handoff")
    mpi, _, _, _ = get_stats_from_dict(mpi_runtime, "BASE (BLOCKING) MPI")
    async_mpi, _, _, _ = get_stats_from_dict(async_mpi_runtime, "ASYNC MPI (OPT 1)")
    async_omp_mpi, _, _, _ = get_stats_from_dict(async_omp_mpi_runtime, "ASYNC MPI + OpenMP (OPT 2)")

    grid_sizes = list(serial_runtimes.keys())

    ax.plot(grid_sizes, serial, marker='o', linestyle='-', linewidth=2, label='Serial')
    ax.plot(grid_sizes, openmp, marker='o', linestyle='-', linewidth=2, label='OpenMP (128 Threads)')
    ax.plot(grid_sizes, gpu, marker='o', linestyle='-', linewidth=2, label='OpenMP GPU Hand-off')
    ax.plot(grid_sizes, mpi, marker='o', linestyle='-', linewidth=2, label='MPI (8 Processes)')
    ax.plot(grid_sizes, async_mpi, marker='o', linestyle='-', linewidth=2, label='Async MPI (Opt 1)')
    ax.plot(grid_sizes, async_omp_mpi, marker='o', linestyle='-', linewidth=2, label='Async MPI + OMP (Opt 2)')

    ax.set_title(f"Runtimes of All Implementations for Different Grid Sizes")
    ax.set_xlabel("Grid Sizes (Logarithmic)")
    ax.set_ylabel("Runtime in Seconds (Logarithmic)")

    ax.set_xticks(grid_sizes)
    ax.get_xaxis().set_major_formatter(ScalarFormatter())
    ax.grid(True, which='major', linestyle=':', linewidth=0.8, alpha=0.6)

    # for x, y in zip(process_count, mean_runtime):
    #     ax.annotate(f"{y:.1f}s", (x, y), textcoords="offset points",
    #                 xytext=(0, 8), ha='center', fontsize=11)

    ax.legend(loc='upper left', fontsize=12, frameon=False, bbox_to_anchor=(1.05, 1))

    plt.tight_layout()
    plt.xscale("log")
    plt.yscale("log")
    plt.show()

plot_stuff()