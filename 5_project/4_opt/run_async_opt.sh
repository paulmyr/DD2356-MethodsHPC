#!/bin/bash -l
# The -l above is required to get the full environment with modules

# Set the allocation to be charged for this job
# not required if you have set a default allocation
#SBATCH -A edu25.DD2356

# The name of the script
#SBATCH -J g18pr_async_opt

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
#SBATCH -e elog_project_async_opt

# Output File
#SBATCH --output project_async_opt.txt

# Run the executable named myexe
# and write the output into my output file
# for processes in 1 2 4 8 16 32 64
echo "###### RUNNING WITH ASYNC_OPT CODE ##########"

for processes in 1 2 4 8 16 32 64
do
    echo "########## RUNNING WITH $processes PROCESSES ##########"
    for count in {1..3}
    do
        echo "Run $count"
        srun -n $processes ./fdtd_async_opt.out 6400000
        echo "----------------------------"
    done
done

echo "###### RUNNING WITH BLOCKING MPI CODE ##########"

for processes in 1 2 4 8 16 32 64
do
    echo "########## RUNNING WITH $processes PROCESSES ##########"
    for count in {1..3}
    do
        echo "Run $count"
        srun -n $processes ../3_mpi/fdtd_mpi.out 6400000
        echo "----------------------------"
    done
done

# # Serial Runs
# for count in {1}
# do
#     echo "SERIAL RUN $count"
#     srun -n 1 ./fdtd_serial.out 6400000
#     echo "----------------------------"
# done
