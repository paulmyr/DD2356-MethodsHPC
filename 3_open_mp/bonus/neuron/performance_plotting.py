# For the varying thread count
THREAD_COUNTS = [1, 8, 32, 64, 128]
SERIAL_RUNTIME = [0.003] * len(THREAD_COUNTS)
OMP_OUTPUT = [0.037, 0.530, 0.560, 0.573, 0.679]

# For the varying neuron count
NEURON_COUNT = [256, 512, 1024, 2048, 4196]
SERIAL_NEURON_TIME = [0.001, 0.001, 0.002, 0.005, 0.010]
OMP_NEURON_TIME = [0.281, 0.552, 0.901, 1.116, 1.503]

import matplotlib.pyplot as plt

plt.style.use('seaborn-v0_8-muted') 



fig, ax = plt.subplots(figsize=(10, 6))


# Creating the plot for the varying number of threads. 
# ax.plot(THREAD_COUNTS, SERIAL_RUNTIME, label='Serial', marker='o', linestyle='-', color='#1f77b4', linewidth=2)
# ax.plot(THREAD_COUNTS, OMP_OUTPUT, label='OMP w/ Tasks', marker='s', linestyle='--', color='#ff7f0e', linewidth=2)
# # ax.plot(THREAD_COUNTS, OMP_CRITICAL_OUTPUT, label="OMP w/ Critical Region", marker='p', linestyle='-', color='#8c564b', linewidth=2)

# ax.set_xlabel("Number of Threads", fontsize=14, fontweight='bold', color='darkblue')
# ax.set_ylabel("Runtime (seconds)", fontsize=14, fontweight='bold', color='darkblue')
# ax.set_title("Comparison of Serial and OMP Nueron Firing Runtimes", fontsize=16, fontweight='bold')

# ax.grid(True, which="both", linestyle='--', alpha=0.7)
# ax.tick_params(axis='both', labelsize=12, width=1.2)

# # Uncomment this to have legend inside the box
# # ax.legend(loc='upper right', fontsize=12, frameon=False)

# # Uncomment this to have the legend outside the box
# ax.legend(loc='upper left', fontsize=12, frameon=False, bbox_to_anchor=(1.05, 1))

# plt.tight_layout()

# plt.show()
# plt.clf()

# Creating the plot for the varying number of neurons
# ax.plot(NEURON_COUNT, SERIAL_NEURON_TIME, label='Serial', marker='o', linestyle='-', color='#1f77b4', linewidth=2)
# ax.plot(NEURON_COUNT, OMP_NEURON_TIME, label='OMP w/ Tasks (64 Threads)', marker='s', linestyle='--', color='#ff7f0e', linewidth=2)
# # ax.plot(THREAD_COUNTS, OMP_CRITICAL_OUTPUT, label="OMP w/ Critical Region", marker='p', linestyle='-', color='#8c564b', linewidth=2)

# ax.set_xlabel("Number of Neurons", fontsize=14, fontweight='bold', color='darkblue')
# ax.set_ylabel("Runtime (seconds)", fontsize=14, fontweight='bold', color='darkblue')
# ax.set_title("Runtime Comparison on Varying Number of Neurons", fontsize=16, fontweight='bold')

# ax.grid(True, which="both", linestyle='--', alpha=0.7)
# ax.tick_params(axis='both', labelsize=12, width=1.2)

# # Uncomment this to have legend inside the box
# # ax.legend(loc='upper right', fontsize=12, frameon=False)

# # Uncomment this to have the legend outside the box
# ax.legend(loc='upper left', fontsize=12, frameon=False, bbox_to_anchor=(1.05, 1))

# plt.tight_layout()

# plt.show()