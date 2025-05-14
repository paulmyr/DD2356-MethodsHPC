#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <mpi.h>

#define STEPS 5000 // Time steps
#define C 1.0   // Wave speed
#define DT 0.01 // Time step
#define DX 1.0  // Grid spacing

double *u, *u_prev;

void initialize(int N) {
    for (int i = 0; i < N; i++) {
        u[i] = sin(2.0 * M_PI * i / N);
        u_prev[i] = u[i];
    }
}

void compute_step(int N) {
    double u_next[N];
    // Explicitly setting u_next[0] and u_next[N-1] to 0 as they are not set in the first loop.
    // This (value of 0) seems to be the value they are getting right now, but this removes ambiguity
    // and possible garbage values. A post about this was made on the discussion forum.
    u_next[0] = 0, u_next[N-1] = 0;

    for (int i = 1; i < N - 1; i++) {
        u_next[i] = 2.0 * u[i] - u_prev[i] + C * C * DT * DT / (DX * DX) * (u[i+1] - 2.0 * u[i] + u[i-1]);
    }
    for (int i = 0; i < N; i++) {
        u_prev[i] = u[i];
        u[i] = u_next[i];
    }
}

void write_output(int step, int N) {
    char filename[50];
    sprintf(filename, "outputs/serial/wave_output_serial_%d.txt", step);
    FILE *f = fopen(filename, "w");
    for (int i = 0; i < N; i++) {
        fprintf(f, "%f\n", u[i]);
    }
    fclose(f);
}

int main(int argc, char** argv) {
    int rank, nprocs;
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    int N;

    if (argc < 2) {
        if (rank == 0) {
            printf("Usage: %s <N divisible by 64>. Using default N of 16000\n", argv[0]);
        }
        N = 16000;
    } else {
        // We assume that IF provided, N is a multiple of 64
        N = atoi(argv[1]);
    }
    u = malloc(N * sizeof(double)), u_prev = malloc(N * sizeof(double));

    MPI_Comm_size(MPI_COMM_WORLD, &nprocs);
    printf("MPI rank %d out of %d processes.\n", rank, nprocs);

    initialize(N);
    
    double start = MPI_Wtime();

    for (int step = 0; step < STEPS; step++) {
        compute_step(N);
        // if (step % 500 == 0) write_output(step, N);
    }

    double end = MPI_Wtime();

    // Write final state to ensure it is correct
    // write_output(STEPS+1, N);

    MPI_Finalize();
    free(u);
    free(u_prev);

    if(rank==0)
      printf("[SERIAL] Simulation complete (%d size, %d steps). Took: %.6f seconds\n", N, STEPS, end - start);
    return 0;
}
