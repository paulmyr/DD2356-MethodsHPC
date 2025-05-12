#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <mpi.h>

#define N 320 // Grid size
#define STEPS 100  // Simulation steps

#define SEND_NORTH_TAG 100
#define SEND_SOUTH_TAG 101
#define SEND_EAST_TAG 102
#define SEND_WEST_TAG 103
#define SEND_NW_TAG 104
#define SEND_SW_TAG 105
#define SEND_NE_TAG 106
#define SEND_SE_TAG 107

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
                total_grid[(row * N) + col] = rand() % 2; 
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
        MPI_Irecv(grid, 1, recv_subarray, 0, 0, MPI_COMM_WORLD, &request);
        MPI_Wait(&request, MPI_STATUS_IGNORE);
        MPI_Type_free(&recv_subarray);
    }

    // FOR DEBUGGING: Print to verify correct thing was received
    // int coords[2];
    // MPI_Cart_coords(cart_comm, process_rank, 2, coords);

    // printf("[Process %d] Responsible for (%d, %d). Received: \n", process_rank, coords[0], coords[1]);
    // for (int i = 0; i < local_rows+2; i++) {
    //     for (int j = 0; j < local_cols+2; j++) {
    //         printf("%d ", grid[get_index(i, j, local_cols+2)]);
    //     }
    //     printf("\n");
    // }
    // printf("\n\n");
    // fflush(stdout);
}


void perform_halo_exchange(int local_rows, int local_cols, MPI_Comm cart_comm, MPI_Datatype column) {
    int up, down, left, right;
    int dims[2], period[2], coords[2];
    int rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    // We only care about dims and coords here
    MPI_Cart_get(cart_comm, 2, dims, period, coords);

    // Get the up and down neighbours. We assume that the top-left coordinate is (0, 0)
    MPI_Cart_shift(cart_comm, 0, 1, &up, &down);
    MPI_Cart_shift(cart_comm, 1, 1, &left, &right);

    // Get the ranks of the processes which have the diagonal neighbour.
    // Will be used to send and receive the corner cells
    int nw, ne, sw, se;
    int diag[2];
    
    // Get the top-left (ie, north-west) corner
    diag[0] = (coords[0] - 1 + dims[0]) % dims[0];
    diag[1] = (coords[1] - 1 + dims[1]) % dims[1];
    MPI_Cart_rank(cart_comm, diag, &nw);

    // Get the top-right (ie, north-east) corner
    diag[0] = (coords[0] - 1 + dims[0]) % dims[0];
    diag[1] = (coords[1] + 1) % dims[1];
    MPI_Cart_rank(cart_comm, diag, &ne);

    // Get the bottom-left (ie, south-west) corner
    diag[0] = (coords[0] + 1) % dims[0];
    diag[1] = (coords[1] - 1 + dims[1]) % dims[1];
    MPI_Cart_rank(cart_comm, diag, &sw);

    // Get the bottom-right (ie, south-east) corner
    diag[0] = (coords[0] + 1) % dims[0];
    diag[1] = (coords[1] + 1) % dims[1];
    MPI_Cart_rank(cart_comm, diag, &se);

    // 16 Requests: 8 things to send, 8 things to receive
    MPI_Request requests[16];

    MPI_Irecv(&grid[get_index(0, 1, local_cols+2)], local_cols, MPI_INT, up, SEND_SOUTH_TAG, cart_comm, &requests[0]);
    MPI_Irecv(&grid[get_index(local_rows+1, 1, local_cols+2)], local_cols, MPI_INT, down, SEND_NORTH_TAG, cart_comm, &requests[1]);
    MPI_Irecv(&grid[get_index(1, local_cols+1, local_cols+2)], 1, column, right, SEND_WEST_TAG, cart_comm, &requests[2]);   
    MPI_Irecv(&grid[get_index(1, 0, local_cols+2)], 1, column, left, SEND_EAST_TAG, cart_comm, &requests[3]);
    // Receives of corners
    MPI_Irecv(&grid[get_index(0, 0, local_cols+2)], 1, MPI_INT, nw, SEND_SE_TAG, cart_comm, &requests[4]);
    MPI_Irecv(&grid[get_index(0, local_cols+1, local_cols+2)], 1, MPI_INT, ne, SEND_SW_TAG, cart_comm, &requests[5]);
    MPI_Irecv(&grid[get_index(local_rows+1, 0, local_cols+2)], 1, MPI_INT, sw, SEND_NE_TAG, cart_comm, &requests[6]);
    MPI_Irecv(&grid[get_index(local_rows+1, local_cols+1, local_cols+2)], 1, MPI_INT, se, SEND_NW_TAG, cart_comm, &requests[7]);
    
    // All sends later 
    // Sends of "bulk" data
    MPI_Isend(&grid[get_index(1, 1, local_cols+2)], local_cols, MPI_INT, up, SEND_NORTH_TAG, cart_comm, &requests[8]);
    MPI_Isend(&grid[get_index(local_rows, 1, local_cols+2)], local_cols, MPI_INT, down, SEND_SOUTH_TAG, cart_comm, &requests[9]);
    MPI_Isend(&grid[get_index(1, local_cols, local_cols+2)], 1, column, right, SEND_EAST_TAG, cart_comm, &requests[10]);
    MPI_Isend(&grid[get_index(1, 1, local_cols+2)], 1, column, left, SEND_WEST_TAG, cart_comm, &requests[11]);
    // Sends of corners
    MPI_Isend(&grid[get_index(1, 1, local_cols+2)], 1, MPI_INT, nw, SEND_NW_TAG, cart_comm, &requests[12]);
    MPI_Isend(&grid[get_index(1, local_cols, local_cols+2)], 1, MPI_INT, ne, SEND_NE_TAG, cart_comm, &requests[13]);
    MPI_Isend(&grid[get_index(local_rows, 1, local_cols+2)], 1, MPI_INT, sw, SEND_SW_TAG, cart_comm, &requests[14]);
    MPI_Isend(&grid[get_index(local_rows, local_cols, local_cols+2)], 1, MPI_INT, se, SEND_SE_TAG, cart_comm, &requests[15]);


    // Wait for everything to finish
    MPI_Waitall(16, requests, MPI_STATUSES_IGNORE);   
}


/**
 * Prints the grid in the correct order. Should not be used when timing, only for debugging purposes and to verify that
 *  the output is correct. All processes send their data to the process with rank 0, which then prints the 
 * grid in the correct order
 */
void print_grid(int process_rank, int dims[2], MPI_Comm cart_comm, int local_rows, int local_cols, int step) {
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
        sprintf(filename, "outputs/parallel/gol_output_parallel_%d.txt", step);
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

int count_neighbors(int x, int y, int local_cols) {
    int sum = 0;
    for (int i = -1; i <= 1; i++) {
        for (int j = -1; j <= 1; j++) {
            if (i == 0 && j == 0) continue;
            // Since we have the ghost cells to help us now, no need
            // for the modulo and the wrap-around.
            int nx = x + i;
            int ny = y + j;
            sum += grid[get_index(nx, ny, local_cols + 2)];
        }
    }
    return sum;
}

void update(int local_rows, int local_cols) {
    for (int i = 0; i < local_rows; i++) {
        for (int j = 0; j < local_cols; j++) {

            int neighbors = count_neighbors(i+1, j+1, local_cols);
            if (grid[get_index(i+1, j+1, local_cols+2)] == 1 && (neighbors < 2 || neighbors > 3)) {
                new_grid[get_index(i+1, j+1, local_cols+2)] = 0;
            } else if (grid[get_index(i+1, j+1, local_cols+2)] == 0 && neighbors == 3) {
                new_grid[get_index(i+1, j+1, local_cols+2)] = 1;
            } else {
                new_grid[get_index(i+1, j+1, local_cols+2)] = grid[get_index(i+1, j+1, local_cols+2)];
            }
        
        }
    }
    for (int i = 0; i < local_rows; i++) {
        for (int j = 0; j < local_cols; j++) {
            grid[get_index(i+1, j+1, local_cols+2)] = new_grid[get_index(i+1, j+1, local_cols+2)];
        }
    }
}

/**
 * Debugging utility to help print the local grid for the provided process. Has the option
 * of including halos for more information
 */
void print_local_grid(int rank, int rows, int cols, int include_halos, MPI_Comm cart_comm) {
    int coords[2];
    MPI_Cart_coords(cart_comm, rank, 2, coords);

    printf("Rank %d grid @ (%d, %d):\n", rank, coords[0], coords[1]);
    for (int i = 0; i < rows + 2; i++) {
        for (int j = 0; j < cols + 2; j++) {
            if ((i == 0 || i == rows + 1 || j == 0 || j == cols + 1)) {
                if (include_halos) {
                    printf("[%4d] ", grid[i * (cols + 2) + j]);  // Halo cells in brackets
                }

            } else {
                printf(" %4d  ", grid[i * (cols + 2) + j]);
            }
        }
        printf("\n");
    }
    printf("\n");
}

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

    // Create the column data type once and re-use it for halo-exchanges
    MPI_Datatype column;
    MPI_Type_vector(local_rows, 1, local_cols + 2, MPI_INT, &column);
    MPI_Type_commit(&column);

    initialize_and_send_grids(rank, dims, cart_comm, local_rows, local_cols);


    for (int step = 0; step < STEPS; step++) {
        perform_halo_exchange(local_rows, local_cols, cart_comm, column);
        update(local_rows, local_cols);

        MPI_Barrier(cart_comm);

        if (step % 10 == 0) print_grid(rank, dims, cart_comm, local_rows, local_cols, step);
    }
    


    MPI_Type_free(&column);
    free(grid);
    free(new_grid);
    MPI_Finalize();
    return 0;
}