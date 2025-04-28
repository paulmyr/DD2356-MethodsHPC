#!/bin/bash -l
#SBATCH --job-name=compile_jobs       # Job name
#SBATCH -A edu25.DD2356
#SBATCH -p shared
#SBATCH --ntasks-per-node=1           # Tasks
#SBATCH --cpus-per-task=4             # CPUs
#SBATCH --nodes=1                     # Nodes
#SBATCH -e error_file.e               # Error file
#SBATCH --time=00:05:00               # Time limit for the job

module load gcc
export OMP_NUM_THREADS=4

# Compile the corresponding file into an object file
srun -n 1 gcc -fopenmp a3/ex1/hello_world.c -o a3/ex1/hello_world.out

# continue after compile
srun -n 1 a3/ex1/hello_world.out > a3/ex1/output.txt
(srun -n 1 hwloc-ls --of svg) > a3/ex1/topology.svg