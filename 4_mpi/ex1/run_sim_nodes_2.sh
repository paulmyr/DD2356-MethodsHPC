#!/bin/bash -l
# The -l above is required to get the full environment with modules

# Set the allocation to be charged for this job
# not required if you have set a default allocation
#SBATCH -A edu25.DD2356

# The name of the script
#SBATCH -J dd2356_a4_ex1_2nodes

# The partition
#SBATCH -p shared

# 10 hours wall clock time will be given to this job
#SBATCH -t 3:00:00

# Total number of MPI tasks (processes)
#SBATCH --ntasks=32                 

# Number of nodes
#SBATCH --nodes 2

# Number of MPI processes per node
#SBATCH --ntasks-per-node 16

# CPUs per task
#SBATCH --cpus-per-task 1

# Error file
#SBATCH -e elog_dd2356_a4_ex1_2_nodes

# Output File
#SBATCH --output a4_ex1_output_2_nodes.txt

# Run the executable named myexe
# and write the output into my output file
echo "################# RUNNING ACROSS 2 NODES, 16 TASKS PER NODE, 32 TASKS TOTAL #################"
for count in {1..3}
do
    echo "Run $count"
    srun ./halo_parallel.out 6400000
    echo "----------------------------"
done