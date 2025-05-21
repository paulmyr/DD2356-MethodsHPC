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
ml openmpi/5.0.0-gcc12.2.0
ml libfabric_vars/1.0.0
ml python
source venv/bin/activate

# due to warning: warning: libfabric.so.1, needed by /pdc/software/23.12/other/openmpi/openmpi-5.0.0-gcc12.2.0/install/lib/libmpi.so, not found (try using -rpath or -rpath-link)
export LD_LIBRARY_PATH=/pdc/software/23.12/eb/software/miniconda3/24.7.1-0-cpeGNU-23.12/lib:$LD_LIBRARY_PATH


# Compile the corresponding file into an object file
# -lm links math library 
srun -n 1 mpicc 5_project/4_mpi/mpi_impl.c -o 5_project/4_mpi/mpi_impl.o -lm 

# mem debugging
#srun -n 3 valgrind -s  --track-origins=yes 5_project/4_mpi/mpi_impl.o 2> errors.txt

# continue after compile
srun -n 4 5_project/4_mpi/mpi_impl.out > 5_project/4_mpi/mpi_impl.txt
(srun -n 1 hwloc-ls --of svg) > 5_project/4_mpi/serial_topology.svg
