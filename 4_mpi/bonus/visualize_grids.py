import numpy as np
import matplotlib.pyplot as plt
import glob
import argparse

parser = argparse.ArgumentParser(description="Plotting Game of Life")
parser.add_argument("--mode", choices=["parallel", "serial"], required=True, help="Which outputs you want to plot")
args = parser.parse_args()


files = sorted(glob.glob(f"outputs/{args.mode}/gol_output_{args.mode}_*.txt"))

for file in files:
    data = np.loadtxt(file)
    plt.imshow(data, cmap='binary', origin='lower')
    plt.title(f"Game of Life - {file}")
    plt.pause(0.5)

plt.show()
