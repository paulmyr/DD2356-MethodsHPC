compile:
	cc -o fdtd_serial.out fdtd_serial.c 
	cc -o fdtd_async_opt.out fdtd_async_opt.c
	cc -o fdtd_async_omp_opt.out -fopenmp fdtd_async_omp_opt.c

compile_local:
	mpicc -o fdtd_serial.out fdtd_serial.c 
	mpicc -o fdtd_async_opt.out fdtd_async_opt.c

clean:
	rm -rf fdtd_serial.out fdtd_async_opt.out fdtd_async_omp_opt.out serial_output.txt opt_output.txt
