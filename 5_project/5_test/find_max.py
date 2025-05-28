import numpy as np
import matplotlib.pyplot as plt

# OPENMP
print("OpenMP implementation")
serial_openmp_readings = "5_project/2_openmp/outputs/serial/fdtd_serial_E_1001.txt"
parallel_gpu_readings = "5_project/2_openmp/outputs/parallel_gpu/fdtd_parallel_E_1001.txt"
parallel_openmp_readings = "5_project/2_openmp/outputs/parallel_omp/fdtd_parallel_E_1001.txt"

serial_openmp_arr = np.loadtxt(serial_openmp_readings)
serial_argmax_openmp = np.argmax(serial_openmp_arr)
serial_max_indices = np.where(serial_openmp_arr == serial_openmp_arr[serial_argmax_openmp])[0]

parallel_arr_gpu = np.loadtxt(parallel_gpu_readings)
parallel_argmax_gpu = np.argmax(parallel_arr_gpu)
parallel_max_indices_gpu = np.where(parallel_arr_gpu == parallel_arr_gpu[parallel_argmax_gpu])[0]

parallel_arr_openmp = np.loadtxt(parallel_openmp_readings)
parallel_argmax_openmp = np.argmax(parallel_arr_openmp)
parallel_max_indices_openmp = np.where(parallel_arr_openmp == parallel_arr_openmp[parallel_argmax_openmp])[0]

print("Serial", serial_argmax_openmp, "with:", serial_openmp_arr[serial_argmax_openmp], 
      "at indices:", serial_max_indices, 
      "Parallel", parallel_argmax_gpu, "with:", parallel_arr_gpu[parallel_argmax_gpu], 
      "at indices:", parallel_max_indices_gpu, 
      "OMP", parallel_argmax_openmp, "with:", parallel_arr_openmp[parallel_argmax_openmp], 
      "at indices:", parallel_max_indices_openmp, "\n")

# MPI
print("MPI implementation")
serial_readings = "5_project/3_mpi/outputs/serial/fdtd_serial_E_1001.txt"
parallel_mpi_readings = "5_project/3_mpi/outputs/parallel/fdtd_parallel_E_1001.txt"

serial_arr = np.loadtxt(serial_readings)
serial_argmax = np.argmax(serial_arr)
serial_max_indices_mpi = np.where(serial_arr == serial_arr[serial_argmax])[0]

parallel_arr_mpi = np.loadtxt(parallel_mpi_readings)
parallel_argmax_mpi = np.argmax(parallel_arr_mpi)
parallel_max_indices_mpi = np.where(parallel_arr_mpi == parallel_arr_mpi[parallel_argmax_mpi])[0]

print("Serial", serial_argmax, "with:", serial_arr[serial_argmax], 
      "at indices:", serial_max_indices_mpi, 
      "Parallel", parallel_argmax_mpi, "with:", parallel_arr_mpi[parallel_argmax_mpi], 
      "at indices:", parallel_max_indices_mpi, "\n")

# OPT
print("Optimization implementation")
serial_readings = "5_project/4_opt/outputs/serial/fdtd_serial_E_1001.txt"
parallel_async_readings = "5_project/4_opt/outputs/parallel_async/fdtd_parallel_E_1001.txt"
parallel_async_omp_readings = "5_project/4_opt/outputs/parallel_async_omp/fdtd_parallel_E_1001.txt"

serial_arr = np.loadtxt(serial_readings)
serial_argmax = np.argmax(serial_arr)
serial_max_indices_opt = np.where(serial_arr == serial_arr[serial_argmax])[0]

parallel_arr = np.loadtxt(parallel_async_readings)
parallel_argmax = np.argmax(parallel_arr)
parallel_max_indices_async = np.where(parallel_arr == parallel_arr[parallel_argmax])[0]

parallel_arr_omp = np.loadtxt(parallel_async_omp_readings)
parallel_argmax_omp = np.argmax(parallel_arr_omp)
parallel_max_indices_omp = np.where(parallel_arr_omp == parallel_arr_omp[parallel_argmax_omp])[0]

print("Serial", serial_argmax, "with:", serial_arr[serial_argmax], 
      "at indices:", serial_max_indices_opt, 
      "Parallel", parallel_argmax, "with:", parallel_arr[parallel_argmax], 
      "at indices:", parallel_max_indices_async, 
      "OMP", parallel_argmax_omp, "with:", parallel_arr_omp[parallel_argmax_omp], 
      "at indices:", parallel_max_indices_omp, "\n")

fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(14, 10))

# OpenMP
axes[0, 0].plot(serial_openmp_arr)
axes[0, 0].set_title("Serial OpenMP")
axes[0, 0].set_xlabel("Index")
axes[0, 0].set_ylabel("Value")

axes[1, 0].plot(parallel_arr_gpu)
axes[1, 0].set_title("Parallel OpenMP GPU")
axes[1, 0].set_xlabel("Index")
axes[1, 0].set_ylabel("Value")

axes[0, 1].plot(parallel_arr_openmp)
axes[0, 1].set_title("Parallel OpenMP")
axes[0, 1].set_xlabel("Index")
axes[0, 1].set_ylabel("Value")

# MPI
axes[2, 0].plot(serial_arr)
axes[2, 0].set_title("Serial MPI")
axes[2, 0].set_xlabel("Index")
axes[2, 0].set_ylabel("Value")

axes[2, 1].plot(parallel_arr_mpi)
axes[2, 1].set_title("Parallel MPI")
axes[2, 1].set_xlabel("Index")
axes[2, 1].set_ylabel("Value")

# Optimization
axes[3, 1].plot(parallel_arr_omp)
axes[3, 1].set_title("Opt Parallel Async with OpenMP")
axes[3, 1].set_xlabel("Index")
axes[3, 1].set_ylabel("Value")

axes[3, 0].plot(parallel_arr)
axes[3, 0].set_title("Opt Parallel Async")
axes[3, 0].set_xlabel("Index")
axes[3, 0].set_ylabel("Value")

fig.delaxes(axes[1, 1])

plt.tight_layout()
plt.savefig("5_project/5_test/verification_plot.png")
plt.show()