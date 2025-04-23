#!/bin/bash -l
# The -l above is required to get the full environment with modules

# Set the allocation to be charged for this job
# not required if you have set a default allocation
#SBATCH -A edu25.DD2356

# The name of the script
#SBATCH -J dd2356_a3_dftw_parallel_some_cores

# The partition
#SBATCH -p shared

# 10 hours wall clock time will be given to this job
#SBATCH -t 1:00:00

# Number of nodes
#SBATCH --nodes 1

# Number of MPI processes per node
#SBATCH --ntasks-per-node 1

# CPUs per taskxq
# Handout says we need 32 Dardel Cores: we assume this means PHYSICAL cores.
# So, this means 64 logical CPUs
#SBATCH --cpus-per-task 64

# Error file
#SBATCH -e elog_dd2356_a3_dftw_parallel_some_cores

for threads in 1 32 64 128
do
    echo "----------------------------------"
    echo "Running with $threads threads"
    export OMP_NUM_THREADS=$threads
    for i in {1..10}
    do
        echo "#### RUN ####"
        srun -n 1 ../dftw_parallel
    done
done
echo "----------------------------------"
echo "Ran with 64 Logical CPUs"
echo "----------------------------------"