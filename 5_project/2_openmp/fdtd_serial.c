#include <math.h>
#include <omp.h>
#include <stdio.h>
#include <stdlib.h>

// #define NX 6400000         // Total number of spatial points
#define NSTEPS 1000 // Number of time steps
#define DX 1.0      // Spatial step size
#define DT 0.5      // Time step size (should satisfy the CFL condition)
#define PI 3.141592653589793

// Function to initialize the electric field with a Gaussian pulse
void initialize_fields(double *E, double *H, int NX) {
  // Center the Gaussian pulse in the middle of the domain
  double center = NX * DX / 2.0;
  for (int i = 0; i < NX; i++) {
    double x = i * DX;
    E[i] = exp(-0.005 * (x - center) * (x - center));
    H[i] = 0.0;
  }
}

// Function to update the magnetic field H
void update_H(double *E, double *H, int NX) {
  // Update H from 0 to NX-2 (using forward differences)
  for (int i = 0; i < NX - 1; i++) {
    H[i] = H[i] + (DT / DX) * (E[i + 1] - E[i]);
  }
  // Simple absorbing boundary condition:
  H[NX - 1] = H[NX - 2];
}

// Function to update the electric field E
void update_E(double *E, double *H, int NX) {
  // Update E from 1 to NX-1 (using backward differences)
  for (int i = 1; i < NX; i++) {
    E[i] = E[i] + (DT / DX) * (H[i] - H[i - 1]);
  }
  // Simple absorbing boundary condition:
  E[0] = E[1];
}

void print_to_file(double *E, double *H, int NX, int step) {
  // Print the global grid now to file
  char filename_E[50], filename_H[50];
  sprintf(filename_E, "outputs/serial/fdtd_serial_E_%d.txt", step);
  sprintf(filename_H, "outputs/serial/fdtd_serial_H_%d.txt", step);
  FILE *f_E = fopen(filename_E, "w"), *f_H = fopen(filename_H, "w");
  for (int i = 0; i < NX; i++) {
    fprintf(f_E, "%f\n", E[i]);
    fprintf(f_H, "%f\n", H[i]);
  }
  fclose(f_E);
  fclose(f_H);
}

int main(int argc, char **argv) {
  int NX;

  if (argc < 2) {
    printf("Usage: %s <NX divisible by 64>. Using default N of 16000\n",
           argv[0]);
    NX = 16000;
  } else {
    // We assume that IF provided, N is a multiple of 64
    NX = atoi(argv[1]);
  }

  // Allocate fields
  double *E = (double *)malloc(NX * sizeof(double));
  double *H = (double *)malloc(NX * sizeof(double));
  if (E == NULL || H == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    return 1;
  }

  // Initialize fields
  initialize_fields(E, H, NX);

  double start_time = omp_get_wtime();

  // Main FDTD loop
  for (int t = 0; t < NSTEPS; t++) {
    update_H(E, H, NX);
    update_E(E, H, NX);

    // if (t % 100 == 0) {
    //     print_to_file(E, H, NX, t);
    // }
  }

  // print_to_file(E, H, NX, NSTEPS + 1);
  double end_time = omp_get_wtime();

  printf("[SERIAL] Time Taken (%d grid, %d steps): %f\n", NX, NSTEPS,
         end_time - start_time);

  free(E);
  free(H);

  return 0;
}
