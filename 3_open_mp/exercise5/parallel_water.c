#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#define N 500  // Grid size
#define ITER 1000  // Number of iterations
#define DT 0.01  // Time step
#define DX 1.0   // Grid spacing
// TODO: I think we need to vary thread counts here by setting the OMP_NUM_THREADS environment
// 	 variable when running on Dardel. Look at ex3 batch scripts for example
#define THREADS 4

double h[N][N], u[N][N], v[N][N];

void initialize() {
    #pragma omp parallel for collapse(2) schedule(guided, 100)
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++) {
            h[i][j] = 1.0;
            u[i][j] = 0.0;
            v[i][j] = 0.0;
        }
}

void compute() {
    #pragma omp parallel for collapse(2) schedule(guided, 100)
    for (int iter = 0; iter < ITER; iter++) {
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
    FILE *f = fopen("parallel_output.txt", "w");
    #pragma omp parallel for collapse(2) schedule(guided, 100)
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            fprintf(f, "%f ", h[i][j]); // race cond shouldn't be a problem here
        }
        //fprintf(f, "\n"); //line leads to error
    }
    fclose(f);
}

int main() {
    initialize();
    double t_start = omp_get_wtime();
    compute();
    double t_end = omp_get_wtime();
    double t_comp = t_end - t_start;
    // write_output();
    // printf("Tstart: %d, Tend %d", t_start, t_end);
    printf("[PARALLEL] Computation completed in: %.3f seconds.\n", t_comp);
    return 0;
}
