#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>

#define NUM_RUNS 10
// Array size is 10^8 elements
#define ARR_SIZE 100000000

// New type with padding
typedef struct {
    // The actual value of the sum
    double sum_val;
    // Cache-line size on dardel is 64 bytes, per "srun getconf LEVEL1_DCACHE_LINESIZE" command.
    // So, 56 extra bytes to ensure that each local sum is on another cache line (since double is 8 bytes)
    char padding[56];  
} LocalSums;

double omp_local_no_sharing_sum(double *x, size_t size) {
  int MAX_THREADS = omp_get_max_threads();
  double final_sum = 0.0;
  LocalSums local_sum[MAX_THREADS]; 
  
  // OMP to compute the local sums
  #pragma omp parallel shared(local_sum)
  {
    int id = omp_get_thread_num();
    local_sum[id].sum_val = 0.0;
    #pragma omp for
        for (size_t i = 0; i < size; i++) {
            local_sum[id].sum_val += x[i];
        }
  }

  // Simple serial C to compute the global sum
  final_sum = 0.0;
  for (int i = 0; i < MAX_THREADS; i++) {
    final_sum += local_sum[i].sum_val;
  }


  return final_sum;
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

    printf("OMP w/ LOCAL SUM (NO SHARING)\n");
    printf("NUMBER OF THREADS TO RUN WITH: %d.\n", omp_get_max_threads());
    for (int i = 0; i < NUM_RUNS; i++) {
        double start = omp_get_wtime();

        curr_sum = omp_local_no_sharing_sum(arr, ARR_SIZE);

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
