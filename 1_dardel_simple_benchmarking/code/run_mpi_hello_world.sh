#!/bin/bash -l
# The -l above is required to get the full environment with modules

# TASKNAME="dd2356_e1"
# DATE=$(date '+%Y%m%d%H%M%S')

# Set the allocation to be charged for this job
# not required if you have set a default allocation
#SBATCH -A edu25.DD2356

# The name of the script is myjob
#SBATCH -J dd2356_e1

# The partition
#SBATCH -p shared

# 10 hours wall clock time will be given to this job
#SBATCH -t 1:00:00

# Number of nodes
#SBATCH --nodes 1

# Number of MPI processes per node
#SBATCH --ntasks-per-node 128

# CPUs per task
#SBATCH --cpus-per-task 1

# Error file
#SBATCH -e elog_d2356_e1

# Run the executable named myexe
# and write the output into my output file
srun ./mpi_hello_world.out > log_dd2356_e1
