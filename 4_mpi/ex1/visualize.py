import numpy as np
import matplotlib.pyplot as plt
import glob
import argparse

parser = argparse.ArgumentParser(description="Plotting Wave Equations")
parser.add_argument("--mode", choices=["parallel", "serial"], required=True, help="Which outputs you want to plot")
args = parser.parse_args()

files = sorted(glob.glob(f"outputs/{args.mode}/wave_output_{args.mode}_*.txt"))

for file in files:
    data = np.loadtxt(file)
    plt.plot(data, label=f"Time step {file.split('_')[-1].split('.')[0]}")

plt.xlabel("Grid Point")
plt.ylabel("Wave Amplitude")
plt.title("Wave Equation Evolution")
plt.legend()
plt.show()
