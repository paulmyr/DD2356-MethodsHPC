#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <mpi.h>

#define STEPS 5000 // Time steps
#define C 1.0   // Wave speed
#define DT 0.01 // Time step
#define DX 1.0  // Grid spacing

double *u, *u_prev;

void compute_step(int local_size, int chunk_resp, int dims) {
    double *u_next = NULL;
    if (chunk_resp == 0) {
        // In this case, the first index actually holding data (u[1]) will remain unchanged. 
        u_next = malloc((local_size - 1) * sizeof(double));

        // In the serial version, we start at index 1. If this is the first chunk, this means that we 
        // Start at index 2 (index 0 is for the halo, index 1 for the actual value, and so index 2 for the value 
        // where we start at in the serial code).
        for (int i = 2; i < local_size + 1; i++) {
            u_next[i-2] = 2.0 * u[i] - u_prev[i] + C * C * DT * DT / (DX * DX) * (u[i+1] - 2.0 * u[i] + u[i-1]);
        }

        // Copy over the result from u_next over to u, but offsetting by 2 because of the same reasons above
        for (int i = 0; i < local_size-1; i++) {
            u_prev[i+2] = u[i+2];
            u[i+2] = u_next[i];
        }

        // We maintain u[1] = 0 here. This is because in the serial code, u_next[0] is assigned to u[0] in the 
        // second for-loop, even though u_next[0] was not initialized by the starter code. So, we make the 
        // assumption that u[0] = 0 always in the starter code (and make the same assumption here). 
        u[1] = 0;
    } else if (chunk_resp == dims - 1) {
        // In this case, the last index actually holding data (u[local_size]) will remain unchanged
        u_next = malloc((local_size - 1) * sizeof(double));

        // In the serial version, we end at N-1. So if we're working with the last chunk here, we need to end
        // at local_size - 1 (local_size stores the last element, local_size + 1 stores the halo)
        for (int i = 1; i < local_size; i++) {
            u_next[i-1] = 2.0 * u[i] - u_prev[i] + C * C * DT * DT / (DX * DX) * (u[i+1] - 2.0 * u[i] + u[i-1]);
        }

        for (int i = 0; i < local_size - 1; i++) {
            u_prev[i+1] = u[i+1];
            u[i+1] = u_next[i];
        }

        // For same reason as above, we set u[local_size] = 0 explicitly;
        u[local_size] = 0;
    } else {
        // Is a chunk in the middle, so there is a 1:1 corelation between u_next and u
        u_next = malloc(local_size * sizeof(double));

        // We want to avoid the halos for u and u_prev, so iterate from 1 to local_size
        for (int i = 1; i < local_size + 1; i++) {
            u_next[i-1] = 2.0 * u[i] - u_prev[i] + C * C * DT * DT / (DX * DX) * (u[i+1] - 2.0 * u[i] + u[i-1]);
        }

        // Copy over the result from u_next to u_prev
        for (int i = 0; i < local_size; i++) {
            u_prev[i+1] = u[i+1];
            u[i+1] = u_next[i];
        }
    }

    // In all cases, u_next would be allocated. So safe to free here
    free(u_next);
}

/**
 * Responsible for initializing and then distributing the 1d Grid of values
 */
void initialize_and_distribute_data(int N, int local_size, int process_id, MPI_Datatype no_hallo_subarray, MPI_Comm cart_comm) {
    double *global_u = NULL, *global_u_prev = NULL;
    if (process_id == 0) {
        // Process 0 responsible for initializing the entire array
        global_u = malloc(N * sizeof(double)), global_u_prev = malloc(N * sizeof(double));
        for (int i = 0; i < N; i++) {
            global_u[i] = sin(2.0 * M_PI * i / N);
            // global_u[i] = i;
            global_u_prev[i] = global_u[i];
        }
    }

    // We will use the custom subtype to avoid having to create a copy
    MPI_Scatter(global_u, local_size, MPI_DOUBLE, u, 1, no_hallo_subarray, 0, cart_comm);
    MPI_Scatter(global_u_prev, local_size, MPI_DOUBLE, u_prev, 1, no_hallo_subarray, 0, cart_comm);

    if (process_id == 0) {
        free(global_u);
        free(global_u_prev);
    }
}

/**
 * For debugging purposes: Responsible for printing the local chunk with or without halos
 */
void print_local_chunk(int local_size, int process_id, int include_halos) {
    printf("[Process %d] Current Local Copy: \n", process_id);
    for (int i = 0; i < local_size + 2; i++) {
        if (i == 0 || i == local_size + 1) {
            if (include_halos) {
                printf("[%4f] ", u[i]);
            }
        } else {
            printf("%4f ", u[i]);
        }
    }
    printf("\n");
    fflush(stdout);
}

/**
 * Responsible for performing the halo-exchange. We only perform the halo_exchange for the u array,
 * Since only that needs the left/right grid values
 */
void perform_halo_exchange(MPI_Comm cart_comm, int local_size) {
    int left, right;
    // We know that cart_comm does not wrap around. So, it could be possible that one of left or right
    // is MPI_PROC_NULL. If that is the case, however, Sendrecv should be able to handle it.
    MPI_Cart_shift(cart_comm, 0, 1, &left, &right);

    // Send to the right neighbour, receive from the left neighbour
    MPI_Sendrecv(&u[local_size], 1, MPI_DOUBLE, right, 0,  // Send to right
                 &u[0], 1, MPI_DOUBLE, left, 0, // Receive from left
                 cart_comm, MPI_STATUS_IGNORE);

    // Send to left neighbour, receive from right neighbour
    MPI_Sendrecv(&u[1], 1, MPI_DOUBLE, left, 1, // Send to left
                &u[local_size + 1], 1, MPI_DOUBLE, right, 1, // Receive from right
                cart_comm, MPI_STATUS_IGNORE);
}

void print_grid(int N, int process_id, int dims[1], MPI_Comm cart_comm, int local_size, int step, MPI_Datatype no_hallo_subarray_type) {
    double *full_grid = NULL;
    if (process_id == 0) {
        full_grid = malloc(N * sizeof(double));
    }

    MPI_Gather(u, 1, no_hallo_subarray_type, full_grid, local_size, MPI_DOUBLE, 0, cart_comm);

    if (process_id == 0) {
        // In full_grid, we have an ordering with the help of ranks. However, it could be the case that there
        // isn't a perfect corelation between the rank of the process and the id of the chunk that it was assigned.
        // For this, we manually re-order here. 
        double *final_grid = malloc(N * sizeof(double));
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
            memcpy(&final_grid[curr_chunk * local_size], &full_grid[curr_id * local_size], local_size * sizeof(double));
        }

        // Print the global grid now to file
        char filename[50];
        sprintf(filename, "outputs/parallel/wave_output_parallel_%d.txt", step);
        FILE *f = fopen(filename, "w");
        for (int i = 0; i < N; i++) {
            fprintf(f, "%f\n", final_grid[i]);
        }
        fclose(f);

        // We always free fill_grid because process with id 0 always initializes it as well!
        free(full_grid);
        free(final_grid);
    }
}

int main(int argc, char** argv) {
    int rank, size;
    // This grid is not wrapping around the edges
    int dims[1] = {0}, periods[1] = {0}, chunk_coords[1];
    int N;
    MPI_Comm cart_comm;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    if (argc < 2) {
        if (rank == 0) {
            printf("Usage: %s <N divisible by 64>. Using default N of 16000\n", argv[0]);
        }
        N = 16000;
    } else {
        // We assume that IF provided, N is a multiple of 64
        N = atoi(argv[1]);
    }


    MPI_Comm_size(MPI_COMM_WORLD, &size);

    MPI_Dims_create(size, 1, dims);
    MPI_Cart_create(MPI_COMM_WORLD, 1, dims, periods, 1, &cart_comm);

    // This is the chunk of the 1D array that this process is responsible for
    MPI_Cart_coords(cart_comm, rank, 1, chunk_coords);

    int local_size = N / dims[0];
    // our local arrays -- u, u_prev -- have 2 more elements than local_size, to allow for halos
    u = malloc((local_size + 2) * sizeof(double)), u_prev = malloc((local_size + 2) * sizeof(double));

    // This datatype will be used to efficiently exchange the initial array (without manually copying to 
    // avoid halos)
    MPI_Datatype no_hallo_subarray_type;
    int start[1] = {1}, sub[1] = {local_size}, full_size[1] = {local_size + 2};
    MPI_Type_create_subarray(1, full_size, sub, start, MPI_ORDER_C, MPI_DOUBLE, &no_hallo_subarray_type);
    MPI_Type_commit(&no_hallo_subarray_type);

    // Initialize and scatter the data, waiting till all processes have received it before proceeeding.
    initialize_and_distribute_data(N, local_size, rank, no_hallo_subarray_type, cart_comm);
    MPI_Barrier(cart_comm);

    double start_time, end_time;

    if (rank == 0) {
        start_time = MPI_Wtime();
    }

    for (int step = 0; step < STEPS; step++) {
        perform_halo_exchange(cart_comm, local_size);
        compute_step(local_size, chunk_coords[0], dims[0]);

        MPI_Barrier(cart_comm);

        // if (step % 500 == 0) print_grid(N, rank, dims, cart_comm, local_size, step, no_hallo_subarray_type);
    }    

    if (rank == 0) {
        end_time = MPI_Wtime();
        // printf("[PARALLEL] Run with %d processes (%d size, %d steps). Took: %.6f seconds\n", size, N, STEPS, end_time - start_time);
    }

    MPI_Comm_free(&cart_comm);
    MPI_Type_free(&no_hallo_subarray_type);
    MPI_Finalize();

    free(u);
    free(u_prev);
    return 0;
}
