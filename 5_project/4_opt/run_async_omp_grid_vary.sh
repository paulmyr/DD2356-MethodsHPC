#!/bin/bash -l
# The -l above is required to get the full environment with modules

# Set the allocation to be charged for this job
# not required if you have set a default allocation
#SBATCH -A edu25.DD2356

# The name of the script
#SBATCH -J g18pr_async_omp_grid_vary

# The partition
#SBATCH -p shared

# 10 hours wall clock time will be given to this job
#SBATCH -t 2:00:00

# Number of node
#SBATCH --nodes 4

# Number of MPI processes per node
#SBATCH --ntasks-per-node 4

# CPUs per task
#SBATCH --cpus-per-task 16

# Error file
#SBATCH -e elog_project_async_omp_grid_vary

# Output File
#SBATCH --output project_async_omp_grid_vary.txt

# Run the executable named myexe
# and write the output into my output file
# for processes in 1 2 4 8 16 32 64

num_threads=16
export OMP_NUM_THREADS=$num_threads

# Running with 16 processes because that seemed to give the best runtime in our tests
echo "################# RUNNING ACROSS UPTO 4 NODES WITH 16 processes, 16 THREADS PER PROCESS ##################"
for grid_size in 640 6400 64000 640000 6400000
do
    echo "######## Grid Size: $grid_size ############"
    for count in {1..3}
    do
        echo "Run $count"
        srun -n 16 ./fdtd_async_omp_opt.out $grid_size
        echo "----------------------------"
    done
done
