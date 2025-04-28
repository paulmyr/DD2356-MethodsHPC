import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("output.txt")
plt.imshow(data, cmap='viridis', origin='lower')
plt.colorbar(label='Water Height')
plt.title('Shallow Water Simulation Result')
plt.show()
plt.savefig("a3/ex5/static/plot.png")