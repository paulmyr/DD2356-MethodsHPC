#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <mpi.h>

#define N 4  // Grid size
#define STEPS 100  // Simulation steps

// Instead of 2D arrays, we use a single pointer for the grids
// They will be in contiguous blocks of memory. 
// So, grid[i][j] should instead be grid[(i * num_cols) + j] for eg
int *grid, *new_grid;

// Helper method to get the index into a 1d of an array given rows and cols
int get_index(int row, int col, int max_cols) {
    return row * max_cols + col;
}

/**
 * If process with rank 0:
 *      Initializes the global grid and sends the relevant chunks to the other processes
 * If process with rank > 0: 
 *      Received the chunk from the process with rank 0 (only the grid, NOT the halos)
 */
void initialize_and_send_grids(int process_rank, int dims[2], MPI_Comm cart_comm, int local_rows, int local_cols) {
    int *total_grid = NULL;

    if (process_rank == 0) {
        total_grid = malloc(N * N * sizeof(int));
        // Seed to ensure similar output
        srand(42);

        // Allocate enough space (not for the halos though)
        int *total_grid = malloc(N * N * sizeof(int));
        int total_processes = dims[0] * dims[1];
        int coords[2], start[2], sub[2], full_size[2] = {N, N};

        // Initialize the entire grid
        for (int row = 0; row < N; row++) {
            for (int col = 0; col < N; col++) {
                // total_grid[(row * N) + col] = rand() % 2; 
                total_grid[(row * N) + col] = row * N + col; 
            }
        }

        // No need to send to yourself so just copy. Note that we leave room for the ghost cells
        MPI_Cart_coords(cart_comm, 0, 2, coords);
        start[0] = coords[0] * local_rows, start[1] = coords[1] * local_cols;
        for (int i = 0; i < local_rows; i++) {
            for (int j = 0; j < local_cols; j++) {
                grid[get_index(i+1, j+1, local_cols+2)] = total_grid[get_index(start[0] + i, start[1] + j, N)];
            }
        }


        // Send chunks to all the processes
        MPI_Request *requests = malloc((total_processes - 1) * sizeof(MPI_Request));
        for (int process_id = 1; process_id < total_processes; process_id++) {
            // Determine the coordinates of the current process
            MPI_Cart_coords(cart_comm, process_id, 2, coords);

            // To make it easier to send chunks, we'll create a data-type. This is because
            // the chunks we need to send won't really be contiguous in memory at times. 
            // The other option is manually copying, but let's try and avoid that as much as we can :) 
            MPI_Datatype subarray;
            start[0] = coords[0] * local_rows, start[1] = coords[1] * local_cols;
            sub[0] = local_rows, sub[1] = local_cols;

            MPI_Type_create_subarray(2, full_size, sub, start, MPI_ORDER_C, MPI_INT, &subarray);
            MPI_Type_commit(&subarray);
            
            MPI_Isend(total_grid, 1, subarray, process_id, 0, MPI_COMM_WORLD, &requests[process_id - 1]);
            MPI_Type_free(&subarray);

        }

        MPI_Waitall(total_processes - 1, requests, MPI_STATUSES_IGNORE);
        free(requests);
        free(total_grid);
    } else {
        // When receiving, we first receive into a local buffer, then we manually copy into a the grid
        MPI_Datatype recv_subarray;
        int start[2] = {1, 1}; // Leave the top-right for the halo
        int sub[2] = {local_rows, local_cols};
        int full_size[2] = {local_rows + 2, local_cols + 2};
        MPI_Type_create_subarray(2, full_size, sub, start, MPI_ORDER_C, MPI_INT, &recv_subarray);
        MPI_Type_commit(&recv_subarray);

        MPI_Request request;
        // int *recv_buff = malloc(local_rows * local_cols * sizeof(int));
        MPI_Irecv(grid, 1, recv_subarray, 0, 0, MPI_COMM_WORLD, &request);
        MPI_Wait(&request, MPI_STATUS_IGNORE);
        MPI_Type_free(&recv_subarray);
    }

    // FOR DEBUGGING: Print to verify correct thing was received
    int coords[2];
    MPI_Cart_coords(cart_comm, process_rank, 2, coords);

    printf("[Process %d] Responsible for (%d, %d). Received: \n", process_rank, coords[0], coords[1]);
    for (int i = 0; i < local_rows+2; i++) {
        for (int j = 0; j < local_cols+2; j++) {
            printf("%d ", grid[get_index(i, j, local_cols+2)]);
        }
        printf("\n");
    }
    printf("\n\n");
    fflush(stdout);
}


/**
 * Prints the grid in the correct order. Should not be used when timing, only for debugging purposes and to verify that
 *  the output is correct. All processes send their data to the process with rank 0, which then prints the 
 * grid in the correct order
 */
void print_grid(int process_rank, int dims[2], MPI_Comm cart_comm, int local_rows, int local_cols) {
    if (process_rank == 0) {
        int *total_grid = malloc(N * N * sizeof(int));
        int total_processes = dims[0] * dims[1];
        int start[2], sub[2], coords[2], full_size[2] = {N, N};

        MPI_Cart_coords(cart_comm, 0, 2, coords);
        start[0] = coords[0] * local_rows, start[1] = coords[1] * local_cols;

        // Copy the data of this process first, SKIPPING the halos
        for (int i = 0; i < local_rows; i++) {
            for (int j = 0; j < local_cols; j++) {
                total_grid[get_index(start[0] + i, start[1] + j, N)] = grid[get_index(i + 1, j + 1, local_cols+2)];
            }
        }

        // Receive and copy over the stuff from the other processes
        MPI_Request *requests = malloc((total_processes - 1) * sizeof(MPI_Request));
        for (int process_id = 1; process_id < total_processes; process_id++) {
            MPI_Cart_coords(cart_comm, process_id, 2, coords);

            MPI_Datatype recv_subarray;
            start[0] = coords[0] * local_rows, start[1] = coords[1] * local_cols;
            sub[0] = local_rows, sub[1] = local_cols;
            MPI_Type_create_subarray(2, full_size, sub, start, MPI_ORDER_C, MPI_INT, &recv_subarray);
            MPI_Type_commit(&recv_subarray);

            MPI_Irecv(total_grid, 1, recv_subarray, process_id, 0, MPI_COMM_WORLD, &requests[process_id - 1]);
            MPI_Type_free(&recv_subarray);
        }

        MPI_Waitall(total_processes - 1, requests, MPI_STATUSES_IGNORE);

        // Print the global grid now to file
        char filename[50];
        sprintf(filename, "gol_output.txt");
        FILE *f = fopen(filename, "w");
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                fprintf(f, "%d ", total_grid[get_index(i, j, N)]);
            }
            fprintf(f, "\n");
        }
        fclose(f);
        free(requests);
        free(total_grid);
    } else {
        MPI_Datatype send_subarray;
        int start[2] = {1, 1};
        int sub[2] = {local_rows, local_cols};
        int full_size[2] = {local_rows + 2, local_cols + 2};
        MPI_Type_create_subarray(2, full_size, sub, start, MPI_ORDER_C, MPI_INT, &send_subarray);
        MPI_Type_commit(&send_subarray);

        MPI_Request request;
        MPI_Isend(grid, 1, send_subarray, 0, 0, MPI_COMM_WORLD, &request);
        MPI_Wait(&request, MPI_STATUS_IGNORE);
        MPI_Type_free(&send_subarray);
    }
}

// int count_neighbors(int x, int y) {
//     int sum = 0;
//     for (int i = -1; i <= 1; i++) {
//         for (int j = -1; j <= 1; j++) {
//             if (i == 0 && j == 0) continue;
//             int nx = (x + i + N) % N;
//             int ny = (y + j + N) % N;
//             sum += grid[nx][ny];
//         }
//     }
//     return sum;
// }

// void update() {
//     for (int i = 0; i < N; i++) {
//         for (int j = 0; j < N; j++) {
//             int neighbors = count_neighbors(i, j);
//             if (grid[i][j] == 1 && (neighbors < 2 || neighbors > 3)) {
//                 new_grid[i][j] = 0;
//             } else if (grid[i][j] == 0 && neighbors == 3) {
//                 new_grid[i][j] = 1;
//             } else {
//                 new_grid[i][j] = grid[i][j];
//             }
//         }
//     }
//     for (int i = 0; i < N; i++) {
//         for (int j = 0; j < N; j++) {
//             grid[i][j] = new_grid[i][j];
//         }
//     }
// }

// void write_output(int step) {
//     char filename[50];
//     sprintf(filename, "gol_output_%d.txt", step);
//     FILE *f = fopen(filename, "w");
//     for (int i = 0; i < N; i++) {
//         for (int j = 0; j < N; j++) {
//             fprintf(f, "%d ", grid[i][j]);
//         }
//         fprintf(f, "\n");
//     }
//     fclose(f);
// }

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);
    int rank, size;
    int dims[2] = {0, 0}, periods[2] = {1, 1}, chunk_coords[2];
    MPI_Comm cart_comm;

    // Housekeeping to get info about size and rank
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    // Create the 2D topology, mapping it to different processes.
    MPI_Dims_create(size, 2, dims);
    MPI_Cart_create(MPI_COMM_WORLD, 2, dims, periods, 1, &cart_comm);

    // Get the chunk coordinates in the 2D grid for the current process
    MPI_Cart_coords(cart_comm, rank, 2, chunk_coords);

    // Determine local row and column size that each process is responsible for computing
    // based on the dimensions assigned by MPI.
    // NOTE: We will assume that N will be perfectly divisible by the number of processes. 
    int local_rows = N / dims[0], local_cols = N / dims[1];
    // NOTE: We malloc for ghost cell values as well
    grid = malloc((local_rows + 2) * (local_cols + 2) * sizeof(int));
    new_grid = malloc((local_rows + 2) * (local_cols + 2) * sizeof(int));

    initialize_and_send_grids(rank, dims, cart_comm, local_rows, local_cols);
    print_grid(rank, dims, cart_comm, local_rows, local_cols);


    
    // initialize();
    // for (int step = 0; step < STEPS; step++) {
    //     update();
    //     if (step % 10 == 0) write_output(step);
    // }
    

    free(grid);
    free(new_grid);
    MPI_Finalize();
    return 0;
}