#include <cblas.h>
#include <math.h>
#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

#define N 1000 // Matrix size

double mysecond() {
  struct timeval tp;
  struct timezone tzp;
  int i;

  i = gettimeofday(&tp, &tzp);
  return ((double)tp.tv_sec + (double)tp.tv_usec * 1.e-6);
}

void initialize(double *matrix, double *vector) {
  for (int i = 0; i < N * N; i++) {
    matrix[i] = (double)(i % 100) / 10.0;
  }
  for (int i = 0; i < N; i++) {
    vector[i] = (double)(i % 50) / 5.0;
  }
}

int main(int argc, char *argv[]) {
  // init MPI
  MPI_Init(&argc, &argv);

  double tstart, tend;
  int rank_root = 0;
  int mpi_size, mpi_rank;
  MPI_Comm_size(MPI_COMM_WORLD, &mpi_size);
  MPI_Comm_rank(MPI_COMM_WORLD, &mpi_rank);

  int chunk_size = (int)ceil(
      (float)N / (float)mpi_size); // Not sure if both type castings are needed.
  int n_padded = chunk_size * mpi_size; // padding

  if (mpi_rank == rank_root) {
    printf("Running with %d processes.\n", mpi_size);
    printf("chunk_size is %d, n_padded is %d.\n", chunk_size, n_padded);
    tstart = mysecond();
  }

  double *working_matrix = (double *)malloc(sizeof(double) * chunk_size * N);
  double *working_result = (double *)malloc(sizeof(double) * chunk_size);

  double *vector =
      (double *)malloc(sizeof(double) * N); // ALL processes need full vector!

  if (mpi_rank == rank_root) {
    double *matrix = (double *)malloc(sizeof(double) * n_padded * N);
    initialize(matrix, vector);

    MPI_Scatter(matrix, chunk_size * N, MPI_DOUBLE, working_matrix,
                chunk_size * N, MPI_DOUBLE, rank_root, MPI_COMM_WORLD);

    free(matrix);
  } else {
    // Don't allocate mem of non root processes
    MPI_Scatter(NULL, 0, MPI_DOUBLE, working_matrix, chunk_size * N, MPI_DOUBLE,
                rank_root, MPI_COMM_WORLD);
  }
  // distribute vector to all processes.
  MPI_Bcast(vector, N, MPI_DOUBLE, rank_root, MPI_COMM_WORLD);

  // Perform matrix-vector multiplication using BLAS
  // cblas_dgemv(CblasRowMajor, CblasNoTrans, N, N, 1.0, matrix, N, vector, 1,
  // 0.0, result, 1);
  cblas_dgemv(CblasRowMajor, CblasNoTrans, chunk_size, N, 1.0, working_matrix,
              N, vector, 1, 0.0, working_result, 1);

  if (mpi_rank == rank_root) {
    double *result = (double *)malloc(N * sizeof(double));

    MPI_Gather(working_result, chunk_size, MPI_DOUBLE, result, chunk_size,
               MPI_DOUBLE, rank_root, MPI_COMM_WORLD);

    // Write output to file
    FILE *f = fopen("blas_output.txt", "w");
    for (int i = 0; i < N; i++) {
      fprintf(f, "%f\n", result[i]);
    }
    fclose(f);

    tend = mysecond();
    printf("BLAS matrix-vector multiplication completed in %f sec.\n",
           tend - tstart);

    free(result);
  } else {
    MPI_Gather(working_result, chunk_size, MPI_DOUBLE, NULL, 0, MPI_DOUBLE,
               rank_root, MPI_COMM_WORLD);
  }

  free(working_matrix);
  free(working_result);
  free(vector);

  MPI_Finalize();
  return 0;
}
