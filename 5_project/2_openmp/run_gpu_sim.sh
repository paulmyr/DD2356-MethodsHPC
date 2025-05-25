#!/bin/bash -l
# The -l above is required to get the full environment with modules

# Set the allocation to be charged for this job
# not required if you have set a default allocation
#SBATCH -A edu25.dd2356

# The name of the script is myjob
#SBATCH -J grp18_proj_gpu

# The partition
#SBATCH -p gpu

# 1 hour wall clock time will be given to this job
#SBATCH -t 01:00:00

# Number of nodes
#SBATCH --nodes=1

# Number of MPI processes per node
#SBATCH --ntasks-per-node=1

#SBATCH -e elog_project_simple_gpu
#SBATCH --output project_gpu.txt
#SBATCH --cpus-per-task 1


for grid_size in 640 6400 64000 640000 6400000
do
    echo "######## Grid Size: $grid_size ############"
    for count in {1..3}
    do
        echo "Run $count"
        srun --partition=gpu --ntasks=1 --gpus-per-task=1 ./fdtd_gpu.out $grid_size
        echo "----------------------------"
    done
done

# Serial Runs
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

