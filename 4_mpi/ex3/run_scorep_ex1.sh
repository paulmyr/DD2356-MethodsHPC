#!/bin/bash -l
# The -l above is required to get the full environment with modules

# Set the allocation to be charged for this job
# not required if you have set a default allocation
#SBATCH -A edu25.DD2356

# The name of the script
#SBATCH -J dd2356_a4_ex3_problem1_simple

# The partition
#SBATCH -p shared

# 10 hours wall clock time will be given to this job
#SBATCH -t 2:00:00

# Total number of MPI tasks (processes)
#SBATCH --ntasks=32                 

# Number of nodes
#SBATCH --nodes 4

# Number of MPI processes per node
#SBATCH --ntasks-per-node 8

# CPUs per task
#SBATCH --cpus-per-task 1

# Error file
#SBATCH -e elog_dd2356_a4_ex3_problem1_simple

# Output File
#SBATCH --output a4_ex3_problem1_simple.txt

# Run the executable named myexe
# and write the output into my output file
srun ./halo_parallel.out 6400000

