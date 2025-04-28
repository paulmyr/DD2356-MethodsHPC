#!/bin/bash -l
#SBATCH --job-name=compile_jobs       # Job name
#SBATCH -A edu25.DD2356
#SBATCH -p shared
#SBATCH --ntasks-per-node=1           # Tasks
#SBATCH --cpus-per-task=128           # CPUs
#SBATCH --nodes=1                     # Nodes
#SBATCH -e error_file.e               # Error file
#SBATCH --time=00:20:00               # Time limit for the job
#SBATCH --array=1-120                  # Jobarray

module load gcc
threads=(1 32 64 128)
chunk=(50 75 100 150 200 1000)
grid=(500 1000 2000 4000 8000)
id=$((SLURM_ARRAY_TASK_ID - 1))
thread_num=${threads[$((id % 4))]}
chunk_size=${chunk[$(((id / 4) % 6))]}
grid_size=${grid[$((id / 24))]}

export OMP_NUM_THREADS=$thread_num
export OMP_SCHEDULE="guided,$chunk_size"
export N=$grid_size

# Compile the corresponding file into an object file
srun -n 1 gcc -fopenmp a3/ex5/parallel_water.c -DID=$id -DN=$grid_size -o a3/ex5/guided/parallel_water$id.out 

wait

# continue after compile
srun -n 1 a3/ex5/guided/parallel_water$id.out > a3/ex5/guided/timings$id.txt