#!/bin/bash -l
# The -l above is required to get the full environment with modules

# Set the allocation to be charged for this job
# not required if you have set a default allocation
#SBATCH -A edu25.DD2356

# The name of the script
#SBATCH -J g18pr_serial_grid_vary

# The partition
#SBATCH -p shared

# 10 hours wall clock time will be given to this job
#SBATCH -t 2:00:00

# Number of nodes
#SBATCH --nodes 1

# Number of MPI processes per node
#SBATCH --ntasks-per-node 1

# CPUs per task
#SBATCH --cpus-per-task 1

# Error file
#SBATCH -e elog_project_serial_grid_vary

# Output File
#SBATCH --output project_serial_grid_vary.txt

# Run the executable named myexe
# and write the output into my output file
# for processes in 1 2 4 8 16 32 64

echo "------------- SERIAL RUNS --------------------"
for grid_size in 640 6400 64000 640000 6400000
do
    echo "######## Grid Size: $grid_size ############"
    for count in {1..3}
    do
        echo "SERIAL RUN $count"
        srun -n 1 ./fdtd_serial.out $grid_size
        echo "----------------------------"
    done
done
