#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

#define N 32000 // Matrix size

double mysecond() {
  struct timeval tp;
  struct timezone tzp;
  int i;

  i = gettimeofday(&tp, &tzp);
  return ((double)tp.tv_sec + (double)tp.tv_usec * 1.e-6);
}

void initialize_matrix(double matrix[][N]) {
  for (int i = 0; i < N; i++) {
    for (int j = 0; j < N; j++) {
      matrix[i][j] = i + j * 0.01;
    }
  }
}

void compute_row_sums(double matrix[][N], double *row_sums) {
  for (int i = 0; i < N; i++) {
    row_sums[i] = 0.0;
    for (int j = 0; j < N; j++) {
      row_sums[i] += matrix[i][j];
    }
  }
}

void write_output(double *row_sums) {
  FILE *f = fopen("sequential_row_sums_output.txt", "w");
  for (int i = 0; i < N; i++) {
    fprintf(f, "%f\n", row_sums[i]);
  }
  fclose(f);
}

int main() {
  printf("Running with 1 process.\n");
  double tstart, tend;
  tstart = mysecond();

  double (*matrix)[N] = malloc(sizeof(double) * N * N);
  double *row_sums = malloc(sizeof(double) * N);

  initialize_matrix(matrix);
  compute_row_sums(matrix, row_sums);
  write_output(row_sums);

  tend = mysecond();
  printf("Complete: took %fs.\n", tend - tstart);

  free(matrix);
  free(row_sums);
  matrix = NULL;
  row_sums = NULL;

  return 0;
}
