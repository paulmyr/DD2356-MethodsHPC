#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>

#define NUM_RUNS 10
// Array size is 10^8 elements
#define ARR_SIZE 100000000

double omp_sum(double *x, size_t size) {
  double sum_val = 0.0;
  
  #pragma omp parallel for
    for (size_t i = 0; i < size; i++) {
      sum_val += x[i];
    }

  return sum_val;
}

void generate_random(double *input, size_t size) {
  srand(42); // Setting seed to get consistent results
  for (size_t i = 0; i < size; i++) {
    input[i] = rand() / (double)(RAND_MAX);
  }
}

int main() {
    double times[NUM_RUNS];
    
    double *arr = malloc(ARR_SIZE * sizeof(double));
    generate_random(arr, ARR_SIZE);
    double curr_sum = 0.0;
    // Running the program with 32 threads
    // omp_set_num_threads(32);

    printf("OMP SUM\n");
    printf("NUMBER OF THREADS TO RUN WITH: %d.\n", omp_get_max_threads());
    for (int i = 0; i < NUM_RUNS; i++) {
        double start = omp_get_wtime();

        curr_sum = omp_sum(arr, ARR_SIZE);

        double end = omp_get_wtime();
        times[i] = end - start;
        printf("Run %d: %.6f seconds. Sum was: %.3f\n", i + 1, times[i], curr_sum);
    }

    // Computing the average
    double sum = 0.0;
    for (int i = 0; i < NUM_RUNS; i++) {
        sum += times[i];
    }
    double average = sum / NUM_RUNS;

    // Computing the standard deviation
    double sq_diff_sum = 0.0;
    for (int i = 0; i < NUM_RUNS; i++) {
        sq_diff_sum += (times[i] - average) * (times[i] - average);
    }
    double stddev = sqrt(sq_diff_sum / NUM_RUNS);

    printf("\nAverage time: %.3f seconds\n", average);
    printf("Standard deviation: %f seconds\n", stddev);

    free(arr);
    
    return 0;
}
