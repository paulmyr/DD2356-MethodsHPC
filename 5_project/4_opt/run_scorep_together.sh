#!/bin/bash -l
# The -l above is required to get the full environment with modules

# The name of the script
#SBATCH -J dd2356_scorep_together

#SBATCH -A edu25.DD2356

# The partition
#SBATCH -p shared

# 10 hours wall clock time will be given to this job
#SBATCH -t 2:00:00                

# Number of nodes
#SBATCH --nodes 1

# Number of MPI processes per node
#SBATCH --ntasks-per-node 128

# CPUs per task
#SBATCH --cpus-per-task 1

# Error file
#SBATCH -e elog_dd2356_scorep_together

# Output File
#SBATCH --output scorep_together.txt

# Run profiling for blocking implementation -- 64 processes
# export SCOREP_EXPERIMENT_DIRECTORY=profiling_mpi_64
srun -n 64 ../3_mpi/fdtd_mpi_scorep.out 6400000

# Profiling of blocking implementation -- 8 processes
# export SCOREP_EXPERIMENT_DIRECTORY=profiling_mpi_8
srun -n 8 ../3_mpi/fdtd_mpi_scorep.out 6400000

# Profiling for async implementation -- 64 processes
# export SCOREP_EXPERIMENT_DIRECTORY=profiling_async_64
srun -n 64 ./fdtd_async_opt_scorep.out 6400000

# export SCOREP_EXPERIMENT_DIRECTORY=profiling_async_8
srun -n 8 ./fdtd_async_opt_scorep.out 6400000
