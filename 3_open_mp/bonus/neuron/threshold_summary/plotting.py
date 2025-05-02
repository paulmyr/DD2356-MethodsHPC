import numpy as np
import matplotlib.pyplot as plt

thresholds = [20, 50, 100, 200, 500]

plt.figure(figsize=(8, 5))

for t in thresholds:
    summary_data = np.loadtxt(f"neuron_omp_threshold_{t}.txt", dtype=str)
    fire_counts = np.array([int(row[-2]) for row in summary_data])
    plt.hist(fire_counts, bins=20, edgecolor='black', label=f"Threshold {t}")

    plt.xlabel("Firing Count")
    plt.ylabel("Number of Neurons")
    plt.title(f"Distribution of Neuron Firings for Threshold {t}")
    plt.show()