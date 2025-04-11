#!/bin/bash -l
#SBATCH --job-name=compile_jobs       # Job name
#SBATCH -A edu25.DD2356
#SBATCH -p shared
##SBATCH --array=1-6                   # Array job 
#SBATCH --ntasks-per-node=1           # Tasks
#SBATCH --cpus-per-task=1             # CPUs
#SBATCH --nodes=1                     # Nodes
#SBATCH -e error_file.e               # Error file
#SBATCH --time=00:05:00               # Time limit for the job

# Load any required modules, if needed
# module load gcc

# N = [10e3 - 10e9]
ARRAY=(1000 10000 100000 1000000 10000000 100000000 1000000000)

# Get the index of the current job in the array
# INDEX=$((SLURM_ARRAY_TASK_ID - 1))

# Compile the corresponding file into an object file
srun -n 1 cc a2ex2/roofline_model.c -o a2ex2man/exercise2_[6].out #-D N=${ARRAY[6]}

# continue after compile
srun -n 1 a2ex2man/exercise2_[6].out > a2ex2man/exercise2_[6].txt