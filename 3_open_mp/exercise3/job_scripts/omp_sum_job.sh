#!/bin/bash -l
# The -l above is required to get the full environment with modules

# Set the allocation to be charged for this job
# not required if you have set a default allocation
#SBATCH -A edu25.DD2356

# The name of the script
#SBATCH -J dd2356_a3_omp_sum

# The partition
#SBATCH -p shared

# 10 hours wall clock time will be given to this job
#SBATCH -t 1:00:00

# Number of nodes
#SBATCH --nodes 1

#SBATCH --ntasks-per-node 1

# CPUs per task
#SBATCH --cpus-per-task 128

# Error file
#SBATCH -e elog_dd2356_a3_omp_sum

# Run the executable named myexe
# and write the output into my output file
for threads in 1 2 4 8 16 20 24 28 32 64 128
do
    echo "Running with $threads threads"
    export OMP_NUM_THREADS=$threads
    srun -n 1 ../omp_sum
done

(srun -n 1 hwloc-ls --of svg) > topology.svg
