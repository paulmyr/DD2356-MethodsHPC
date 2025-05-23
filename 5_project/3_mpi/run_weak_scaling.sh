#!/bin/bash -l
# The -l above is required to get the full environment with modules

# Set the allocation to be charged for this job
# not required if you have set a default allocation
#SBATCH -A edu25.DD2356

# The name of the script
#SBATCH -J grp18pr_mpi_weak_scaling

# The partition
#SBATCH -p shared

# 10 hours wall clock time will be given to this job
#SBATCH -t 3:00:00

# Number of nodes
#SBATCH --nodes 1

# Number of MPI processes per node
#SBATCH --ntasks-per-node 64

# CPUs per task
#SBATCH --cpus-per-task 1

# Error file
#SBATCH -e elog_dd2356_project_g18_weak_scaling

# Output File
#SBATCH --output project_mpi_weak_scaling.txt


num_threads=1
export OMP_NUM_THREADS=$num_threads

# This is the size of the subproblem PER PROCESS (remains fixed)
subprocess_problem=100000
echo "WEAK SCALING: SIZE PER PROBLEM IS $subprocess_problem"
# Run the executable named myexe
# and write the output into my output file
for processes in 1 2 4 8 16 32 64
do
    grid_size=$((subprocess_problem * processes))
    echo "########## RUNNING WITH $processes PROCESSES ($num_threads Thread) ##########"
    for count in {1..3}
    do
        echo "Run $count"
        srun -n $processes ./fdtd_mpi.out $grid_size
        echo "----------------------------"
    done
done
