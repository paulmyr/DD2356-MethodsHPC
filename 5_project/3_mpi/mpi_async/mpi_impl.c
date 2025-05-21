#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <mpi.h>

#define NX 400         // Total number of spatial points
#define NSTEPS 1000    // Number of time steps
#define DX 1.0         // Spatial step size
#define DT 0.5         // Time step size (should satisfy the CFL condition)
#define PI 3.141592653589793

//  Custom buffer
typedef struct {double e, h;} Buffer;

// Function to initialize the electric field with a Gaussian pulse
void initialize_fields(double *E, double *H) {
    // Center the Gaussian pulse in the middle of the domain
    double center = NX * DX / 2.0;
    for (int i = 0; i < NX; i++) {
        double x = i * DX;
        E[i] = exp(-0.005 * (x - center) * (x - center));
        H[i] = 0.0;
    }
}

// Function to update the magnetic field H
void update_H(double *E, double *H, int local_N) {
    // Update H from 0 to NX-2 (using forward differences)
    for (int i = 0; i < local_N - 1; i++) {
        H[i] = H[i] + (DT / DX) * (E[i + 1] - E[i]);
    }
    // Simple absorbing boundary condition:
    H[NX - 1] = H[NX - 2];
}

// Function to update the electric field E
void update_E(double *E, double *H, int local_N) {
    // Update E from 1 to NX-1 (using backward differences)
    for (int i = 1; i < local_N; i++) {
        E[i] = E[i] + (DT / DX) * (H[i] - H[i - 1]);
    }
    // Simple absorbing boundary condition:
    E[0] = E[1];
}

void exchange_strides(double *E, double *H, int rank, int nprocs, int local_N, MPI_Datatype e_h_datatype, Buffer rbuf, Buffer sbuf) {
    MPI_Request requests[4];
    MPI_Status status[4];
    
    printf("[%d] Entering exchange_strides with local_N = %d\n", rank, local_N);
    
    // Clear previous values
    //memset(requests, 0, sizeof(MPI_Request) * 4);
    // memset(status, 0, sizeof(MPI_Status) * 4);
    
    // Left boundary handling
    if (rank > 0) {
        printf("[%d] Left boundary: Accessing E[1] and H[1]\n", rank);
        sbuf.e = E[1];
        sbuf.h = H[1];
        
        int tag = 0;
        MPI_Irecv(&rbuf, 1, e_h_datatype, rank - 1, tag, MPI_COMM_WORLD, &requests[0]);
        MPI_Isend(&sbuf, 1, e_h_datatype, rank - 1, tag + 1, MPI_COMM_WORLD, &requests[1]);
        
        printf("[%d] Waiting for left boundary communication\n", rank);
        MPI_Waitall(2, requests, status);
        
        if (status[0].MPI_ERROR != MPI_SUCCESS) {
            printf("[%d] Error in left MPI_Irecv\n", rank);
            MPI_Abort(MPI_COMM_WORLD, 1);
        }
        
        E[0] = rbuf.e;
        H[0] = rbuf.h;
    }
    
    // Right boundary handling
    if (rank < nprocs - 1) {
        printf("[%d] Right boundary: Accessing E[%d] and H[%d]\n", 
               rank, local_N - 1, local_N - 1);
        sbuf.e = E[local_N - 1];
        sbuf.h = H[local_N - 1];
        
        int tag = 0;
        MPI_Irecv(&rbuf, 1, e_h_datatype, rank + 1, tag, MPI_COMM_WORLD, &requests[2]);
        MPI_Isend(&sbuf, 1, e_h_datatype, rank + 1, tag + 1, MPI_COMM_WORLD, &requests[3]);
        
        printf("[%d] Waiting for right boundary communication\n", rank);
        MPI_Waitall(2, requests + 2, status + 2);
        
        if (status[2].MPI_ERROR != MPI_SUCCESS) {
            printf("[%d] Error in right MPI_Irecv\n", rank);
            MPI_Abort(MPI_COMM_WORLD, 1);
        }
        
        E[local_N] = rbuf.e;
        H[local_N] = rbuf.h;
    }
    
    printf("[%d] Completed exchange_strides\n", rank);
}

int main(int argc, char **argv) {

    // Init MPI
    int rank, nprocs;
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &nprocs);
    printf("MPI rank %d out of %d processes.\n", rank, nprocs);
    int local_N = NX / nprocs;

    // debug
    printf("[%d] Memory layout:\n", rank);
    printf("[%d]   NX = %d\n", rank, NX);
    printf("[%d]   nprocs = %d\n", rank, nprocs);
    printf("[%d]   local_N = %d\n", rank, local_N);
    printf("[%d]   E/H array size = %d\n", rank, local_N * sizeof(double));
    
    // Allocate fields
    
    double *E = (double *) malloc(local_N * sizeof(double));
    double *H = (double *) malloc(local_N * sizeof(double));
    if (E == NULL || H == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        MPI_Abort(MPI_COMM_WORLD, 1);
        return 1;
    }
    
    // Initialize fields
    initialize_fields(E, H);
    
    // Create derived datatype to send array items in one call 
    // Type and shape definition
    MPI_Datatype e_h_datatype;
    int block_shape[2] = {1, 1}; // n items per field
    MPI_Datatype types[2] = {MPI_DOUBLE, MPI_DOUBLE}; // each item is type field item
    
    // displacement calculation: https://www.mpi-forum.org/docs/mpi-4.1/mpi41-report/node101.htm
    MPI_Aint addr1, addr2;
    MPI_Get_address(&E[0], &addr1);
    MPI_Get_address(&H[0], &addr2);
    MPI_Aint displacements[2];
    displacements[0] = 0;
    displacements[1] = MPI_Aint_diff(addr1, addr2); // instead of arithm. op as advised in docs above
    
    MPI_Type_create_struct(2, block_shape, displacements, types, &e_h_datatype);
    MPI_Type_commit(&e_h_datatype);

    
    // Start time
    double t_start = MPI_Wtime();

    // Create buffer
    Buffer rbuf;
    Buffer sbuf;
    
    // Main FDTD loop
    for (int t = 0; t < NSTEPS; t++) {
        exchange_strides(E, H, rank, nprocs, local_N, e_h_datatype, rbuf, sbuf);
        update_H(E, H, local_N);
        update_E(E, H, local_N);
    }

    double *E_gather = (double *) malloc(NX * sizeof(double));
    
    if (!E_gather) {
        fprintf(stderr, "Memory allocation failed\n");
        MPI_Abort(MPI_COMM_WORLD, 1);
        return 1;
    }
    
    if (rank == 0) {
        // size = 1 in units of our datatype not byte
        int error = MPI_Gather(E, local_N, MPI_DOUBLE, E_gather, local_N, 
                            MPI_DOUBLE, 0, MPI_COMM_WORLD);
    
        if (error != MPI_SUCCESS) {
            fprintf(stderr, "MPI_Gather failed\n");
            free(E_gather);
            MPI_Abort(MPI_COMM_WORLD, 1);
            return 1;
        }
    }
    
    // Measure time and write output into separate file
    double t_end = MPI_Wtime();
    double t_comp = t_end - t_start;
    


    FILE *file;
    file = fopen("5_project/4_mpi/mpi_timing.txt","r");
    printf("Time: %f \n", t_comp);
    fclose(file);
    
    // Output final snapshot of the electric field for verification
    printf("Final electric field snapshot (first 20 values):\n");
    for (int i = 0; i < 20; i++) {
        printf("%f ", E_gather[i]);        
    }
    printf("\n");
    
    // Free memory and finalize MPI
    free(E);
    free(H);
    free(E_gather);

    MPI_Type_free(&e_h_datatype);
    MPI_Finalize();
    
    return 0;
}