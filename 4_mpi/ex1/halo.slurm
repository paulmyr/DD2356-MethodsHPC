#!/bin/bash -l
#SBATCH --job-name=compile_jobs       # Job name
#SBATCH -A edu25.DD2356
#SBATCH -p shared
#SBATCH --ntasks-per-node=4           # Tasks
#SBATCH --cpus-per-task=1             # CPUs
#SBATCH --nodes=1                     # Nodes
#SBATCH -e error_file.e               # Error file
#SBATCH --time=00:05:00               # Time limit for the job

ml PDC/23.12
ml gcc12.2.0
ml openmpi
ml python
source venv/bin/activate

# Compile the corresponding file into an object file
# -lm links math library
# RUN IN MULTIPLE PROCESSES!
srun -n 1 mpicc 4_mpi/ex1/halo.c -o 4_mpi/ex1/halo.out -lm

# continue after compile
srun -n 4 4_mpi/ex1/halo.out > 4_mpi/ex1/halo_output.txt

#srun -n 1 python 4_mpi/ex1/visualize.py > 4_mpi/ex1/visualize.txt