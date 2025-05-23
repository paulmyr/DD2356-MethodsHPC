#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <mpi.h>

#define NSTEPS 1000    // Number of time steps
#define DX 1.0         // Spatial step size
#define DT 0.5         // Time step size (should satisfy the CFL condition)
#define PI 3.141592653589793

// HALO EXCHANGE CONSTNATS
// Determine when to perform which halo exchange
#define HALO_EXCHANGE_E 420
#define HALO_EXCHANGE_H 690


// The local fields H, E that the process would be responsible for
double *local_H, *local_E;

/**
 * Function to initialize the electric field with a Gaussian pulse and distribute it to other processes
 * Process with rank 0 initializes everything and then distributes it to the other processes. 
 * */ 
void initialize_and_distribute_fields(int NX, int local_size, int process_id, MPI_Comm cart_comm) {
    double *global_H = NULL, *global_E = NULL;

    if (process_id == 0) {
        global_H = malloc(NX * sizeof(double)), global_E = malloc(NX * sizeof(double));
        // Center the Gaussian pulse in the middle of the domain
        double center = NX * DX / 2.0;

        for (int i = 0; i < NX; i++) {
            double x = i * DX;
            global_E[i] = exp(-0.005 * (x - center) * (x - center));
            global_H[i] = 0.0;
        }
    }

    // Custom subtype to exchange the values
    // For the H local copies, we want to leave the left side open to receive elements from the left neighbour
    MPI_Scatter(global_H, local_size, MPI_DOUBLE, local_H + 1, local_size, MPI_DOUBLE, 0, cart_comm);
    // For the E local copies, the right side will remain open to receive elements from the right neighbour
    MPI_Scatter(global_E, local_size, MPI_DOUBLE, local_E + 1, local_size, MPI_DOUBLE, 0, cart_comm);

    if (process_id == 0) {
        free(global_H);
        free(global_E);
    }
}

/**
 * Responsible for performing the halo-exchange. We only perform the halo_exchange for the u array,
 * Since only that needs the left/right grid values
 */
void perform_halo_exchange(MPI_Comm cart_comm, int local_size, int left, int right, int which_halo_exchange) {
    if (which_halo_exchange == HALO_EXCHANGE_H) {
        // ############## EXCHANGES FOR H ######################
        // Send to the right neighbour, receive from the left neighbour
        MPI_Sendrecv(&local_H[local_size], 1, MPI_DOUBLE, right, 0,  // Send to right
                    &local_H[0], 1, MPI_DOUBLE, left, 0, // Receive from left
                    cart_comm, MPI_STATUS_IGNORE);
    } 

    if (which_halo_exchange == HALO_EXCHANGE_E) {
        // ################# EXCHANGES FOR E #####################
        // Send to left neighbour, receive from right neighbour
        MPI_Sendrecv(&local_E[1], 1, MPI_DOUBLE, left, 1, // Send to left
                    &local_E[local_size + 1], 1, MPI_DOUBLE, right, 1, // Receive from right
                    cart_comm, MPI_STATUS_IGNORE);  
    }  
}


// Function to update the magnetic field H
void update_H(int local_size, int chunk_resp, int dims) {
    // All but the last chunk handle things in the same way.
    // For the last chunk, the absorbing boundary condition needs to be adhered to.
    if (chunk_resp == dims - 1) {
        for (int i = 1; i < local_size; i++) {
            local_H[i] = local_H[i] + (DT / DX) * (local_E[i+1] - local_E[i]);
        }
        local_H[local_size] = local_H[local_size-1];
    } else {
        for (int i = 1; i < local_size + 1; i++) {
            local_H[i] = local_H[i] + (DT / DX) * (local_E[i+1] - local_E[i]);
        }
    }
}

// Function to update the electric field E
void update_E(int local_size, int chunk_resp) {
    // All but the first chunk handle things in the same way.
    // For the first chunk, the absorbing boundary condition needs to be adhered to.
    if (chunk_resp == 0) {
        for (int i = 2; i < local_size + 1; i++) {
            local_E[i] = local_E[i] + (DT / DX) * (local_H[i] - local_H[i-1]);
        }
        local_E[1] = local_E[2];
    } else {
        for (int i = 1; i < local_size + 1; i++) {
            local_E[i] = local_E[i] + (DT / DX) * (local_H[i] - local_H[i-1]);
        }
    }
}


void print_grid(int NX, int process_id, int dims[1], MPI_Comm cart_comm, int local_size, int step, int print_to_file) {
    double *full_grid_E = NULL, *full_grid_H = NULL;
    if (process_id == 0) {
        full_grid_E = malloc(NX * sizeof(double));
        full_grid_H = malloc(NX * sizeof(double));
    }

    // Gather the E and H grids at the rank 0 process
    MPI_Gather(local_E + 1, local_size, MPI_DOUBLE, full_grid_E, local_size, MPI_DOUBLE, 0, cart_comm);
    MPI_Gather(local_H + 1, local_size, MPI_DOUBLE, full_grid_H, local_size, MPI_DOUBLE, 0, cart_comm);

    if (process_id == 0) {
        // In full_grid, we have an ordering with the help of ranks. However, it could be the case that there
        // isn't a perfect corelation between the rank of the process and the id of the chunk that it was assigned.
        // For this, we manually re-order here. 
        double *final_grid_E = malloc(NX * sizeof(double)), *final_grid_H = malloc(NX * sizeof(double));
        for (int curr_id = 0; curr_id < dims[0]; curr_id++) {
            // Get the number of the chunk that the current process is responsible for
            int curr_coord[1];
            MPI_Cart_coords(cart_comm, curr_id, 1, curr_coord);
            int curr_chunk = curr_coord[0];

            // Copy from the full_grid to the final_grid
            // Destination: curr_chunk is the chunk that the current process was responsible for. So, gives intended
            //              index of the contents of this process
            // Source     : The elements in full_grid were ordered by the ranks of the processes, so the id of the process
            //              times the number of elements in each chunk is where we'd find the starting point of what to copy                
            memcpy(&final_grid_E[curr_chunk * local_size], &full_grid_E[curr_id * local_size], local_size * sizeof(double));
            memcpy(&final_grid_H[curr_chunk * local_size], &full_grid_H[curr_id * local_size], local_size * sizeof(double));
        }

        if (print_to_file == 1) {
            // Print the global grid now to file
            char filename_E[50], filename_H[50];
            sprintf(filename_E, "outputs/parallel/fdtd_parallel_E_%d.txt", step);
            sprintf(filename_H, "outputs/parallel/fdtd_parallel_H_%d.txt", step);
            FILE *f_E = fopen(filename_E, "w"), *f_H = fopen(filename_H, "w");
            for (int i = 0; i < NX; i++) {
                fprintf(f_E, "%f\n", final_grid_E[i]);
                fprintf(f_H, "%f\n", final_grid_H[i]);
            }
            fclose(f_E);
            fclose(f_H);
        } else {
            // Output final snapshot of the electric field for verification
            // printf("Final electric field snapshot (first 20 values):\n");
            // for (int i = 0; i < NX; i++) {
            //     printf("%f\n", final_grid[i]);
            // }
            // printf("\n");
        }

        // We always free fill_grid because process with id 0 always initializes it as well!
        free(full_grid_E);
        free(final_grid_E);
        free(full_grid_H);
        free(final_grid_H);
    }
}




int main(int argc, char** argv) {
    int rank, size;
    // We do not need to wrap around here
    int dims[1] = {0}, periods[1] = {0}, chunk_coords[1];
    int NX;
    MPI_Comm cart_comm;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    if (argc < 2) {
        if (rank == 0) {
            printf("Usage: %s <NX divisible by 64>. Using default N of 16000\n", argv[0]);
        }
        NX = 16000;
    } else {
        // We assume that IF provided, N is a multiple of 64
        NX = atoi(argv[1]);
    }

    MPI_Comm_size(MPI_COMM_WORLD, &size);

    MPI_Dims_create(size, 1, dims);
    MPI_Cart_create(MPI_COMM_WORLD, 1, dims, periods, 1, &cart_comm);

    MPI_Cart_coords(cart_comm, rank, 1, chunk_coords);
    int local_size = NX / dims[0];

    // Local copies of both E and H only need entities from their right and left neighbours 
    // respectively. However, for a easier 1-1 mapping of the computation loop from the serial version
    // to the parallel version, we allocate BOTH left and right halos so that the E and H arrays are 
    // perfectly aligned. 
    // NOTE: Could potentially be optimized in a better version.
    local_E = malloc((local_size + 2) * sizeof(double)), local_H = malloc((local_size + 2) * sizeof(double));

    // // Create a datatype to efficiently fill the NON-HALO portion of the local arrays for 
    // // each process. This will be used to exchange the initializing data before the simulation.
    // MPI_Datatype no_halo_subarray_type;
    // int start[1] = {1}, sub[1] = {local_size}, full_size[1] = {local_size + 2};
    // MPI_Type_create_subarray(1, full_size, sub, start, MPI_ORDER_C, MPI_DOUBLE, &no_halo_subarray_type);
    // MPI_Type_commit(&no_halo_subarray_type);

    // Initialize and distribute the data to all processes
    initialize_and_distribute_fields(NX, local_size, rank, cart_comm);
    
    double start_time, end_time;

    if (rank == 0) {
        start_time = MPI_Wtime();
    }

    // Determine the left and right neighbour once and re-use this information
    // for performing the halo_exchanges later
    int left, right;
    // We know that cart_comm does not wrap around. So, it could be possible that one of left or right
    // is MPI_PROC_NULL. If that is the case, however, Sendrecv should be able to handle it.
    MPI_Cart_shift(cart_comm, 0, 1, &left, &right);

    // Main FDTD loop
    for (int t = 0; t < NSTEPS; t++) {
        // Exchange HALO for E
        perform_halo_exchange(cart_comm, local_size, left, right, HALO_EXCHANGE_E);
        // Compute H
        update_H(local_size, chunk_coords[0], dims[0]);
        // Exchange HALO for H
        perform_halo_exchange(cart_comm, local_size, left, right, HALO_EXCHANGE_H);
        // Compute E
        update_E(local_size, chunk_coords[0]);

        // Diagnostic Print every 100 steps to verify correctness 
        if (t % 100 == 0) {
            MPI_Barrier(cart_comm);
            print_grid(NX, rank, dims, cart_comm, local_size, t, 1);
        }
    }
    
    MPI_Barrier(cart_comm);

    print_grid(NX, rank, dims, cart_comm, local_size, NSTEPS+1, 1);
    
    if (rank == 0) {
        end_time = MPI_Wtime();
        printf("[PARALLEL] Run with %d processes (%d size, %d steps). Took: %.6f seconds\n", size, NX, NSTEPS, end_time - start_time);
    }


    MPI_Comm_free(&cart_comm);
    // MPI_Type_free(&no_halo_subarray_type);
    MPI_Finalize();

    free(local_H);
    free(local_E);
    return 0;
}