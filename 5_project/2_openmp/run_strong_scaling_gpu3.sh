#!/bin/bash -l
# The -l above is required to get the full environment with modules

#SBATCH -A edu25.DD2356
#SBATCH -J g18pr_gpu_strong_scaling
#SBATCH -p gpu
#SBATCH -t 1:00:00
#SBATCH --nodes 1
#SBATCH --ntasks-per-node 1
#SBATCH --cpus-per-task 1
#SBATCH --gpus-per-task 3
#SBATCH -e elog_project_gpu_strong_scaling3
#SBATCH --output project_gpu_strong_scaling3.txt

# Run the executable named myexe
# and write the output into my output file
##for processes in 1 2 4 8 16 32 64 128 256
for processes in 3
do
    echo "########## RUNNING WITH $processes GPUS ##########"
    for count in {1..3}
    do
        echo "Run $count"
        srun -n 1 gpu.out 6400000
        echo "----------------------------"
    done
done

# Serial Runs
for count in {1..3}
do
    echo "SERIAL RUN $count"
    srun -n 1 serial.out 6400000
    echo "----------------------------"
done
