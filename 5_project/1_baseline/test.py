import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("output.txt")
plt.imshow(data, cmap='viridis', origin='lower')
plt.colorbar(label='E-field')
plt.title('Gaussian Pulse Simulation')
plt.show()
plt.savefig("5_project/1_baseline/test_plot.png")       