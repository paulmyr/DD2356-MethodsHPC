#!/bin/bash -l
#SBATCH --job-name=compile_jobs       # Job name
#SBATCH -A edu25.DD2356
#SBATCH -p shared
#SBATCH --ntasks-per-node=1           # Tasks
#SBATCH --cpus-per-task=1             # CPUs
#SBATCH --nodes=1                     # Nodes
#SBATCH -e error_file.e               # Error file
#SBATCH --time=00:05:00               # Time limit for the job

ml gcc
ml python
source venv/bin/activate

# Compile the corresponding file into an object file
srun -n 1 gcc -fopenmp 5_project/1_baseline/serial.c -o 5_project/1_baseline/serial.out

# continue after compile
srun -n 1 5_project/1_baseline/serial.out > 5_project/1_baseline/serial_benchmark.txt
(srun -n 1 hwloc-ls --of svg) > 4_project/1_baseline/serial_topology.svg

srun -n 1 python 5_project/1_baseline/test.py > 5_project/1_baseline/test_benchmark.txt