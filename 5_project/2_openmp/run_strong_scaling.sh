#!/bin/bash -l
# The -l above is required to get the full environment with modules

#SBATCH -A edu25.DD2356
#SBATCH -J g18pr_omp_strong_scaling
#SBATCH -p shared
#SBATCH -t 1:00:00
#SBATCH --nodes 1
#SBATCH --ntasks-per-node 1
#SBATCH --cpus-per-task 256
#SBATCH -e elog_project_omp_strong_scaling
#SBATCH --output project_omp_strong_scaling.txt

# Run the executable named myexe
# and write the output into my output file
# for processes in 1 2 4 8 16 32 64
for processes in 1 2 4 8 16 32 64 128 256
do
    export OMP_NUM_THREADS=$processes
    echo "########## RUNNING WITH $processes THREADS ##########"
    for count in {1..3}
    do
        echo "Run $count"
        srun -n 1 omp.out 6400000
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
