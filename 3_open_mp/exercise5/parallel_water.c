#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

// #define N 500  // Grid size defined by slurm script
#define ITER 1000  // Number of iterations
#define DT 0.01  // Time step
#define DX 1.0   // Grid spacing

double h[N][N], u[N][N], v[N][N];

void initialize() {
    #pragma omp parallel for collapse(2)
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++) {
            h[i][j] = 1.0;
            u[i][j] = 0.0;
            v[i][j] = 0.0;
        }
}

void compute() {
    for (int iter = 0; iter < ITER; iter++) {
        #pragma omp parallel for collapse(2)
        for (int i = 1; i < N - 1; i++) {
            for (int j = 1; j < N - 1; j++) {
                // no race condition since idx private
                double dudx = (u[i+1][j] - u[i-1][j]) / (2.0 * DX);
                double dvdy = (v[i][j+1] - v[i][j-1]) / (2.0 * DX);
                h[i][j] -= DT * (dudx + dvdy);
            }
        }
    }
}

void write_output() {
    char filename[50];
    printf("Write output id:%d",ID);
    sprintf(filename, "a3/ex5/guided/output%d.txt", ID); // dynamic macro read
    FILE *f = fopen(filename, "w");
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            fprintf(f, "%f ", h[i][j]); // race cond shouldn't be a problem here
        }
        fprintf(f, "\n"); 
    }
    fclose(f);
}

int main() {
    initialize();
    double t_start = omp_get_wtime();
    compute(); 
    double t_end = omp_get_wtime();
    double t_comp = t_end - t_start;
    // printf("Tstart: %f, Tend %f", t_start, t_end);
    printf("Time: %f \n", t_comp);
    const char *N_size = getenv("N");
    const char *schedule = getenv("OMP_SCHEDULE");
    const char *thread_size = getenv("OMP_NUM_THREADS");
    printf("Grid size: %s \n", N_size);
    printf("Schedule: %s \n", schedule);
    printf("Threads: %s \n", thread_size);
    write_output();
    // printf("Computation completed.\n");
    return 0;
}
