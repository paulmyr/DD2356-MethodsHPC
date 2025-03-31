#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    int rank;
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    
    int data = 42;
    double start, end;
    
    for (int size = 1; size <= 1024; size *= 2) {
        if (rank == 0) {
            start = MPI_Wtime();
            MPI_Send(&data, size, MPI_INT, 1, 0, MPI_COMM_WORLD);
            MPI_Recv(&data, size, MPI_INT, 1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            end = MPI_Wtime();
	    // Chaning format-string for bytes to "%lu" to prevent compile-time warning
            printf("Size: %lu Bytes, RTT: %f microseconds\n", size * sizeof(int), (end - start) * 1e6);
	    // Flushing to stdout immediately after printing so that output is available even if program hangs
	    // (see discussion post on canvas under "Performance Modeling & Benchmarking" section)
	    fflush(stdout);
        } else {
            MPI_Recv(&data, size, MPI_INT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            MPI_Send(&data, size, MPI_INT, 0, 0, MPI_COMM_WORLD);
        }
    }
    
    MPI_Finalize();
    return 0;
}
