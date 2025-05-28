import numpy as np
import matplotlib.pyplot as plt

arr0 = np.genfromtxt("./400.txt")
arr1 = np.genfromtxt("./6400.txt")
arr2 = np.genfromtxt("./16000.txt")
arr3 = np.genfromtxt("./64000.txt")
arr4 = np.genfromtxt("./640000.txt")

fig, axes = plt.subplots(5, 1, figsize=(10, 18))

axes[0].plot(arr0, label="400NX gridsize", linestyle='-')
axes[0].set_title("400NX gridsize")
axes[0].set_xlabel("Index")
axes[0].set_ylabel("Value")
axes[0].grid(True)
axes[0].legend()

axes[1].plot(arr1, label="6400NX gridsize", linestyle='-')
axes[1].set_title("6400NX gridsize")
axes[1].set_xlabel("Index")
axes[1].set_ylabel("Value")
axes[1].grid(True)
axes[1].legend()

axes[2].plot(arr2, label="16000NX gridsize", linestyle='-')
axes[2].set_title("16000NX gridsize")
axes[2].set_xlabel("Index")
axes[2].set_ylabel("Value")
axes[2].grid(True)
axes[2].legend()

axes[3].plot(arr3, label="64000NX gridsize", linestyle='-')
axes[3].set_title("64000NX gridsize")
axes[3].set_xlabel("Index")
axes[3].set_ylabel("Value")
axes[3].grid(True)
axes[3].legend()

axes[4].plot(arr4, label="640000NX gridsize", linestyle='-')
axes[4].set_title("640000NX gridsize")
axes[4].set_xlabel("Index")
axes[4].set_ylabel("Value")
axes[4].grid(True)
axes[4].legend()

plt.tight_layout()

plt.savefig("./display_field_subplots.png")
plt.show()