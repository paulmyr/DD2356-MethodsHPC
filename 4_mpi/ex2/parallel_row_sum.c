#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

#include <mpi.h>

#define N 32000 // Matrix size

double mysecond() {
  struct timeval tp;
  struct timezone tzp;
  int i;

  i = gettimeofday(&tp, &tzp);
  return ((double)tp.tv_sec + (double)tp.tv_usec * 1.e-6);
}

void initialize_matrix(double matrix[][N], int num_rows) {
  for (int i = 0; i < N; i++) {
    for (int j = 0; j < N; j++) {
      matrix[i][j] = i + j * 0.01;
    }
  }
  /*
   * not neeeded, because we initialized using calloc!
   * for (int i = N; i < num_rows; i++) {
   *   for (int j = 0; j < N; j++) {
   *     matrix[i][j] = 0.0;
   *   }
   * }
   */
}

int sum_reduce(double rows[], int num_rows) {
  int sum = 0;
  for (int i = 0; i < num_rows; i++) {
    sum += rows[i];
  }
  return sum;
}

void compute_row_sums(double matrix[][N], double row_sums[], int chunk_size) {
  for (int i = 0; i < chunk_size; i++) {
    row_sums[i] = 0.0;
    for (int j = 0; j < N; j++) {
      row_sums[i] += matrix[i][j];
    }
  }
}

void write_output(double row_sums[]) {
  FILE *f = fopen("parallel_row_sums_output.txt", "w");
  for (int i = 0; i < N; i++) {
    fprintf(f, "%f\n", row_sums[i]);
  }
  fclose(f);
}

int main(int argc, char *argv[]) {
  // init MPI
  MPI_Init(&argc, &argv);

  double tstart, tend;
  int root_process = 0;
  int mpi_size, mpi_rank;
  MPI_Comm_size(MPI_COMM_WORLD, &mpi_size);
  MPI_Comm_rank(MPI_COMM_WORLD, &mpi_rank);

  if (mpi_rank == root_process) {
    printf("Running with %d processes.\n", mpi_size);
    tstart = mysecond();
  }

  // Calculate chunk size:
  int chunk_size = (int)ceil((float)N / (float)mpi_size);
  int num_rows = chunk_size * mpi_size; // padding

  double (*matrix)[N] = NULL;
  double (*working_matrix)[N] = malloc(sizeof(double) * chunk_size * N);
  double *local_row_sums = malloc(sizeof(double) * chunk_size);

  if (mpi_rank == root_process) {
    matrix = malloc(sizeof(double) * num_rows * N);
    initialize_matrix(matrix, num_rows);
    MPI_Scatter(matrix, chunk_size * N, MPI_DOUBLE, working_matrix,
                chunk_size * N, MPI_DOUBLE, root_process, MPI_COMM_WORLD);
    free(matrix);
    matrix = NULL; // prevent uaf
  } else {
    MPI_Scatter(NULL, 0, MPI_DOUBLE, working_matrix, chunk_size * N, MPI_DOUBLE,
                root_process, MPI_COMM_WORLD);
  }

  compute_row_sums(working_matrix, local_row_sums, chunk_size);

  if (mpi_rank == root_process) {
    double *row_sums = malloc(sizeof(double) * num_rows);
    MPI_Gather(local_row_sums, chunk_size, MPI_DOUBLE, row_sums, chunk_size,
               MPI_DOUBLE, root_process, MPI_COMM_WORLD);
    // implicit barrier here.
    write_output(row_sums);
    tend = mysecond();
    printf("Complete: took %fs.\n", tend - tstart);
  } else {
    MPI_Gather(local_row_sums, chunk_size, MPI_DOUBLE, NULL, 0, MPI_DOUBLE,
               root_process, MPI_COMM_WORLD);
  }

  int local_result = sum_reduce(local_row_sums, chunk_size);
  int global_result;

  MPI_Reduce(&local_result, &global_result, 1, MPI_INT, MPI_SUM, root_process,
             MPI_COMM_WORLD);

  if (mpi_rank == root_process)
    printf("Row sum total: %d\n", global_result);

  free(working_matrix);
  free(local_row_sums);
  working_matrix = NULL;
  local_row_sums = NULL;

  MPI_Finalize();
  return 0;
}
