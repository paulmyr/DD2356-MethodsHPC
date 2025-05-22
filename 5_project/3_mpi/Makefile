compile:
	cc -o fdtd_serial.out fdtd_serial.c 
	cc -o fdtd_mpi.out -fopenmp fdtd_mpi.c

compile_local:
	mpicc -o fdtd_serial.out fdtd_serial.c 
	mpicc -o fdtd_mpi.out fdtd_mpi.c

clean:
	rm -rf fdtd_mpi.out fdtd_serial.out serial_output.txt mpi_output.txt
