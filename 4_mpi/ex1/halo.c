#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <mpi.h>

#define N 1000 // Grid size
#define STEPS 100 // Time steps
#define C 1.0   // Wave speed
#define DT 0.01 // Time step
#define DX 1.0  // Grid spacing

double u[N], u_prev[N];

void initialize() {
    for (int i = 0; i < N; i++) {
        u[i] = sin(2.0 * M_PI * i / N);
        u_prev[i] = u[i];
    }
}

void compute_step() {
    double u_next[N];
    for (int i = 1; i < N - 1; i++) {
        u_next[i] = 2.0 * u[i] - u_prev[i] + C * C * DT * DT / (DX * DX) * (u[i+1] - 2.0 * u[i] + u[i-1]);
    }
    // shift each result by one
    for (int i = 0; i < N; i++) {
        u_prev[i] = u[i];
        u[i] = u_next[i];
    }
}

void exchange_strides(double *u, int rank, int nprocs, int local_N) {
    // exchange neighbor cell except if borders are met (left and rightmost fields)
    MPI_Status status;
    // left shift
    if (rank > 0){
        MPI_Sendrecv(&u[1], 1, MPI_DOUBLE, rank - 1, 0, // sending part -> left
                     &u[0], 1, MPI_DOUBLE, rank - 1, 0, // receiving part -> left
                     MPI_COMM_WORLD, &status);  
    }
    // left boundary
    else {
        u[0] = u[1]; 
    }

    // right shift
    if (rank < nprocs - 1){
        MPI_Sendrecv(&u[local_N], 1, MPI_DOUBLE, rank + 1, 0, // sending part -> right
                     &u[local_N + 1], 1, MPI_DOUBLE, rank + 1, 0, // receiving part -> right
                     MPI_COMM_WORLD, &status);  
    }
    // right boundary
    else {
        u[local_N + 1] = u[local_N];
    }
}

void write_output(int step, int rank, int local_N) {
    // concat u
    if (rank == 0) {
        double *concat_u = malloc(N * sizeof(double));
        
        // gather all cell values in the concat_u
        // u[1] refers to the start location of data to be sent with size local_N
        MPI_Gather(&u[1], local_N, MPI_DOUBLE, concat_u, local_N, MPI_DOUBLE, 0, MPI_COMM_WORLD);

        char filename[50];
        sprintf(filename, "4_mpi/ex1/wave_output_%d.txt", step);
        FILE *f = fopen(filename, "w");
        for (int i = 0; i < N; i++) {
            fprintf(f, "%f\n", concat_u[i]);
        }
        fclose(f);

        free(concat_u);
    }
}

int main(int argc, char** argv) {
    int rank, nprocs;
    MPI_Init(&argc, &argv);
    double t1 = MPI_Wtime(); // start timing after MPI spawning
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &nprocs);
    printf("MPI rank %d out of %d processes.\n", rank, nprocs);
    if(rank==0)
        initialize();

    int local_N = N / nprocs;
    
    for (int step = 0; step < STEPS; step++) {
        exchange_strides(u, rank, nprocs, local_N);
        compute_step();
        if (step % 10 == 0) write_output(step, rank, local_N);
    }
    double t2 = MPI_Wtime();
    printf("Time %d \n", t2-t1);

    MPI_Finalize();
    
    if(rank==0)
        printf("Simulation complete.\n");
    return 0;
} 