import numpy as np
import matplotlib.pyplot as plt

summary_data = np.loadtxt("neuron_summary_omp.txt", dtype=str)
print(summary_data)
fire_counts = np.array([int(row[-2]) for row in summary_data])

plt.figure(figsize=(8, 5))
plt.hist(fire_counts, bins=20, color='blue', edgecolor='black')
plt.xlabel("Firing Count")
plt.ylabel("Number of Neurons")
plt.title("Distribution of Neuron Firings")
plt.show()