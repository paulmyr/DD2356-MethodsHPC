#!/bin/bash -l
# The -l above is required to get the full environment with modules

# Set the allocation to be charged for this job
# not required if you have set a default allocation
#SBATCH -A edu25.DD2356

# The name of the script
#SBATCH -J dd2356_a3_serial_sum

# The partition
#SBATCH -p shared

# 10 hours wall clock time will be given to this job
#SBATCH -t 1:00:00

# Number of nodes
#SBATCH --nodes 1

# Number of MPI processes per node
#SBATCH --ntasks-per-node 1

# CPUs per task
#SBATCH --cpus-per-task 128

# Error file
#SBATCH -e elog_dd2356_a3_serial_sum

# Run the executable named myexe
# and write the output into my output file
srun -n 1 ../serial_sum
