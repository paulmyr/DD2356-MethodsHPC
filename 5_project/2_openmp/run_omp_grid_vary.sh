#!/bin/bash -l
# The -l above is required to get the full environment with modules

#SBATCH -A edu25.DD2356
#SBATCH -J g18pr_omp_grid_vary
#SBATCH -p shared
#SBATCH -t 1:00:00
#SBATCH --nodes 1
#SBATCH --ntasks-per-node 1
#SBATCH --cpus-per-task 128
#SBATCH -e elog_project_omp_grid_vary
#SBATCH --output project_omp_grid_vary.txt

# Run the executable named myexe
# and write the output into my output file
# for processes in 1 2 4 8 16 32 64

# 128 threads as that seemed to give the best runtime
export OMP_NUM_THREADS=128

for grid_size in 640 6400 64000 640000 6400000
do
    echo "######## Grid Size: $grid_size ############"
    for count in {1..3}
    do
        echo "Run $count"
        srun -n 1 ./fdtd_omp.out $grid_size
        echo "----------------------------"
    done
done