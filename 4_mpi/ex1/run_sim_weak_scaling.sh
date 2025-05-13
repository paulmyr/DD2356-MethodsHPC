#!/bin/bash -l
# The -l above is required to get the full environment with modules

# Set the allocation to be charged for this job
# not required if you have set a default allocation
#SBATCH -A edu25.DD2356

# The name of the script
#SBATCH -J dd2356_a4_ex1_weak

# The partition
#SBATCH -p shared

# 10 hours wall clock time will be given to this job
#SBATCH -t 2:00:00

# Number of nodes
#SBATCH --nodes 1

# Number of MPI processes per node
#SBATCH --ntasks-per-node 64

# CPUs per task
#SBATCH --cpus-per-task 1

# Error file
#SBATCH -e elog_dd2356_a4_ex1_weak

# Output File
#SBATCH --output a4_ex1_weak_scaling_output.txt


# This is the size of the subproblem PER PROCESS (remains fixed)
subprocess_problem=1000
echo "WEAK SCALING: SIZE PER PROBLEM IS $subprocess_problem"
# Run the executable named myexe
# and write the output into my output file
for processes in 1 2 4 8 16 32 64
do
    grid_size=$((subprocess_problem * processes))
    echo "########## RUNNING WITH $processes PROCESSES ##########"
    for count in {1..3}
    do
        echo "Run $count"
        srun -n $processes ./halo_parallel.out $grid_size
        echo "----------------------------"
    done
done
