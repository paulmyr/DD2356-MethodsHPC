compile:
	cc -o fdtd_serial.out fdtd_serial.c 
	cc -o -fopenmp fdtd_opt.out fdtd_opt.c

compile_local:
	mpicc -o fdtd_serial.out fdtd_serial.c 
	mpicc -o fdtd_opt.out fdtd_opt.c

clean:
	rm -rf fdtd_opt.out fdtd_serial.out serial_output.txt opt_output.txt
