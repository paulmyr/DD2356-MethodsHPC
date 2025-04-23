import numpy as np
import matplotlib.pyplot as plt
import argparse


def get_first_number_from_string(input_string):
    """
    Extracts and returns the FIRST numerical value encountered in the string. 
    Precondition: the string MUST have at least one numerical value in it
    """
    return [int(s) for s in input_string.split() if s.isdigit()][0]

def get_parallel_run_info(filename):
    """
    Extracts information from log file (see the job_scripts for format of file)
    and returns a tuple. The FIRST element is a DICTIONARY with the following keys 
    and information:
    
    key             value
    ---             -----
    x_1             the runtimes of the individual runs with x_1 threads
    x_2             the runtimes of the individual runs with x_2 threads
    ...
    x_n             the runtimes of the individual runs with x_n threads

    The SECOND element is the number of cores that experiment was run on

    We assume that we are running the simulation with N=10000 (as described in the handout)
    """
    info_dict = {}
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()

    # Each useful piece of information is separated by the following delimiter
    running_splits = content.split('----------------------------------')
    if running_splits[0] == "":
        running_splits = running_splits[1:]
    if running_splits[-1] == "":
        running_splits = running_splits[:-1]

    # Per the job script, this information should be present between the last 2 sets of delimiters
    # There should only be one digit, thus we are hardcoding and extracting the first array element here
    logical_cpus = get_first_number_from_string(running_splits[-1])
    
    # We have the information about the number of cores now. Going forward,
    # we only need information about the running times
    running_splits = running_splits[:-1]

    for curr_run in running_splits:
        thread_counts = get_first_number_from_string(curr_run.split("\n")[1])
        # individual_run_info = curr_run.split("#### RUN ####")[1:]
        # times = [float(curr_line.split("\n")[2].split(":")[1]) for curr_line in individual_run_info]
        info_dict[thread_counts] = get_individual_run_info(curr_run)
    
    return (info_dict, logical_cpus)

def get_serial_info(filename):
    """
    Does the same thing as `get_parallel_run_info`, but for a serial run (so no threads).
    This only returns an ARRAY of runtimes. Since there is no need to know about the number 
    of cores or the threads (since this is serial, by definition).
    """
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    
    return get_individual_run_info(content)

def get_individual_run_info(run_string):
    """
    Common helper utility that can be used to get the information for an individual run
    for both the parallel and the serial info extractor functions.

    Returns an ARRAY OF RUNTIMES for the current run
    """
    # Using the ...[1:] to skip over newline
    individual_run_info = run_string.split("#### RUN ####")[1:]
    times = [float(curr_line.split("\n")[2].split(":")[1]) for curr_line in individual_run_info]
    return times


def get_average_parallel_runtimes(runtime_info_dict, logical_cpus):
    """
    Given the runtime info dict (in the format returned by `get_parallel_run_info`) and the number
    of logical cpus that the run was completed on, returns a TUPLE.

    The first element is an array of AVERAGE runtimes. 
    The second element is an array of THREAD counts.
    """
    avg_runtimes, thread_counts = [], []
    print(f"######### INFORMATION FOR RUN ON {logical_cpus} LOGICAL CORES #########")
    for thread_count, runtimes in runtime_info_dict.items():
        print(f"Individual Runtimes for {thread_count} thread(s): {runtimes}")
        print(f"Average Runtime: {np.average(runtimes)}")
        print(f"Standard Devation: {np.std(runtimes)}")
        thread_counts.append(thread_count)
        avg_runtimes.append(np.average(runtimes))
    
    print("\n\n")
    return (avg_runtimes, thread_counts)

def get_performance_plot(avg_runtime_all_cores, avg_runtime_some_cores, serial_runtime, threads, all_cores_count, some_cores_count):
    """
    Creates a performance plot (ie, runtime on the y axis, threads on the x axis) given the information above in the arguments
    """
    plt.figure(figsize=(10, 6))

    plt.plot(threads, serial_runtime, marker='o', label='Serial', color='b', linestyle='-', linewidth=2, markersize=8)
    plt.plot(threads, avg_runtime_all_cores, marker='s', label=f'OpenMP ({all_cores_count} logical cores)', color='g', linestyle='--', linewidth=2, markersize=8)
    plt.plot(threads, avg_runtime_some_cores, marker='^', label=f'OpenMP ({some_cores_count} logical cores)', color='r', linestyle='-.', linewidth=2, markersize=8)

    plt.title('Performance Comparison: Serial vs OpenMP', fontsize=16, fontweight='bold')
    plt.xlabel('Number of Threads', fontsize=14)
    plt.ylabel('Runtime (seconds)', fontsize=14)
    # plt.xscale('log') 
    # plt.yscale('log')  
    plt.xticks(threads)  
    plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=12, frameon=False)

    plt.tight_layout()
    plt.show()

def get_speedup_plot(speedup_all_cores, speedup_some_cores, threads, all_cores_count, some_cores_count):
    """
    Creates the speedup chart given the information above. The y axis is the speedup, the x axis is the thread count
    """
    plt.figure(figsize=(10, 6))

    plt.plot(threads, speedup_all_cores, marker='s', label=f'OpenMP ({all_cores_count} logical cores)', color='g', linestyle='--', linewidth=2, markersize=8)
    plt.plot(threads, speedup_some_cores, marker='^', label=f'OpenMP ({some_cores_count} logical cores)', color='r', linestyle='-.', linewidth=2, markersize=8)

    plt.title('OpenMP Speedup Chart (for different cores in setup)', fontsize=16, fontweight='bold')
    plt.xlabel('Number of Threads', fontsize=14)
    plt.ylabel('Speedup', fontsize=14)
    plt.xticks(threads)  
    plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=12, frameon=False)

    plt.tight_layout()
    plt.show() 


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prints and Plots Performance + Speedup DFTW Data Based on Output Files Provided")

    parser.add_argument('serial_output', type=str, help="The location of the output for the serial implementation")
    parser.add_argument('some_core_output', type=str, help="The location of the output for the OpenMP implementation using some cores in the setup (ie, less than 128 logical cores)")
    parser.add_argument('all_core_output', type=str, help="The location of the output for the OpenMP implementation using all cores in the setup (ie, at least 128 logical cores)")

    args = parser.parse_args()


    # This stores the number of threads the parallel programs were run with
    threads = []

    # Information about the serial run
    serial_runtime = get_serial_info(args.serial_output)
    serial_average = np.average(serial_runtime)
    serial_std = np.std(serial_runtime)

    # Parallel Info (on 128 logical CPUs and on 64 logical CPUs)
    runtimes_info_all_cores, num_cpus_all = get_parallel_run_info(args.all_core_output)
    runtimes_info_some_cores, num_cpus_some = get_parallel_run_info(args.some_core_output)

    runtime_avg_all_cores, threads = get_average_parallel_runtimes(runtimes_info_all_cores, num_cpus_all)
    runtime_avg_some_cores, _ = get_average_parallel_runtimes(runtimes_info_some_cores, num_cpus_some)
    runtime_avg_serial = [serial_average] * len(threads)

    all_core_speedup, some_core_speedup = np.asarray(runtime_avg_serial) / np.asarray(runtime_avg_all_cores), np.asarray(runtime_avg_serial) / np.asarray(runtime_avg_some_cores)


    print(f"Thread Counts: {threads}")
    print(f"Avg All Cores: {runtime_avg_all_cores}")
    print(f"Avg Some Cores: {runtime_avg_some_cores}")
    print(f"Avg Serial: {runtime_avg_serial}")
    print(f"All Cores Speedup: {all_core_speedup}")
    print(f"Some Cores Speedup: {some_core_speedup}")

    get_performance_plot(runtime_avg_all_cores, runtime_avg_some_cores, runtime_avg_serial, threads, num_cpus_all, num_cpus_some)
    get_speedup_plot(speedup_all_cores=all_core_speedup, speedup_some_cores=some_core_speedup, threads=threads, all_cores_count=num_cpus_all, some_cores_count=num_cpus_some)

