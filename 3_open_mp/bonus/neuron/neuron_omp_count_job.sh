#!/bin/bash -l
# The -l above is required to get the full environment with modules

# Set the allocation to be charged for this job
# not required if you have set a default allocation
#SBATCH -A edu25.DD2356

# The name of the script
#SBATCH -J dd2356_a3_neuron_omp_nueron_count

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
#SBATCH -e elog_dd2356_a3_neuron_omp_neuron_count

# Output File
#SBATCH --output neuron_omp_count_job.out

# Run the executable named myexe
# and write the output into my output file
export OMP_NUM_THREADS=64

for neuron in 256 512 1024 2048 4196
do
    echo "----------------------------"
    echo "Running with $neuron neurons"
    # Getting both the serial and the parallel runtimes at once
    srun -n 1 ./neuron_omp 0 $neuron 50 "neuron_omp_count_$neuron.txt"
    srun -n 1 ./neuron_serial 0 $neuron 50 "neuron_omp_count_serial_$neuron.txt"
done