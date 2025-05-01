#!/bin/bash -l
# The -l above is required to get the full environment with modules

# Set the allocation to be charged for this job
# not required if you have set a default allocation
#SBATCH -A edu25.DD2356

# The name of the script
#SBATCH -J dd2356_a3_neuron_omp

# The partition
#SBATCH -p shared

# 10 hours wall clock time will be given to this job
#SBATCH -t 2:00:00

# Number of nodes
#SBATCH --nodes 1

# Number of MPI processes per node
#SBATCH --ntasks-per-node 1

# CPUs per task
#SBATCH --cpus-per-task 128

# Error file
#SBATCH -e elog_dd2356_a3_neuron_omp

# Output File
#SBATCH --output neuron_omp_job.out

# Run the executable named myexe
# and write the output into my output file
for threads in 1 8 32 64 128
do
    echo "----------------------------"
    echo "Running with $threads threads"
    export OMP_NUM_THREADS=$threads
    srun -n 1 ./neuron_omp 0 1024 50 "neuron_omp_threads_$threads.txt"
done

# Serial Run
echo "----------------------------"
srun -n 1 ./neuron_serial 0 1024 50 "neuron_omp_threads_serial.txt"