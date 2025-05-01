#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <omp.h>
#include <math.h>


// This is the maximum number of neurons we will have. The actual ones will be provided from the 
// Command line. 
#define NEURONS 8192
#define STEPS 500

// The number of times the simulation is run. Done to get more reasonable time measurements
#define NUM_RUNS 10

double potentials[NEURONS];
int firings[NEURONS];
int random_potential_additions[NEURONS * STEPS];


/**
 * 
 * Simulates neuron firing. Optionally writing to file in each iteration. 
 * The write to file is optional so that file I/O does not interfere with timing when file is not being written to
 */
void simulate_serial(int write_to_file, int number_of_neurons, double threshold) {
    FILE *f;
    if (write_to_file == 1) {
        f = fopen("neuron_output_serial.txt", "w");
    }
    for (int step = 0; step < STEPS; step++) {
        int curr_step = step;
        for (int i = 0; i < number_of_neurons; i++) {
            potentials[i] += random_potential_additions[curr_step*number_of_neurons + i];
            if (potentials[i] > threshold) {
                firings[i]++;
                potentials[i] = 0;  // Reset potential
            }
            if (write_to_file == 1) {
                fprintf(f, "%d %d %f\n", step, i, potentials[i]);
            }
        }
    }

    if (write_to_file == 1) {
        fclose(f);
    }
}

int main(int argc, char *argv[]) {
    if (argc < 5) {
        printf("Usage: ./neuron_omp <0 or 1 to write to file> <number of neurons> <threshold> <summary_file_name>\n");
        return 1;
    }

    // No error checking: We assume that the correct types are provided here
    int write_to_file = atoi(argv[1]);
    int number_of_neurons = atoi(argv[2]);
    if (number_of_neurons > NEURONS) {
        printf("Maximum number of neurons allowed: %d\n", NEURONS);
        return 1;
    }
    double threshold;
    sscanf(argv[3],"%lf", &threshold);
    char *summary_file_name = argv[4];

    printf("SERIAL OMP SIMULATION. NUMBER OF NEURONS: %d. FIRING THRESHOLD: %.3f\n", number_of_neurons, threshold);
    double times[NUM_RUNS];

    srand(42);
    for (int i = 0; i < number_of_neurons; i++) {
        potentials[i] = rand() % 20;
        firings[i] = 0;
    }

    // Initialize the random potential additions, since using rand() is NOT THREAD SAFE
    // This will help us ensure we get the same output in each call (both threaded and normal versions)
    for (int i = 0; i < number_of_neurons * STEPS; i++) {
        random_potential_additions[i] = rand() % 10;
    }

    // Simulating NUM_RUNS times
    for (int i = 0; i < NUM_RUNS; i++) {
        double t_start = omp_get_wtime();
        simulate_serial(write_to_file, number_of_neurons, threshold);
        double t_end = omp_get_wtime();
        
        times[i] = t_end - t_start;
        printf("Run %d: %.6f seconds\n", i + 1, times[i]);
    }

    // Computing the Average
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

    FILE *fsummary = fopen(summary_file_name, "w");
    for (int i = 0; i < number_of_neurons; i++) {
        fprintf(fsummary, "Neuron %d fired %d times\n", i, firings[i]);
    }
    fclose(fsummary);
    
    return 0;
}
