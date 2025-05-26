import numpy as np
import matplotlib.pyplot as plt
import multiprocessing

# Constants
DX = 1.0  
DT = 1.0
PI = 3.141592653589793
NSTEPS = 1000

def initialize_fields(NX, DX):
    E = np.zeros(NX)
    H = np.zeros(NX)
    center = NX * DX / 2.0
    
    for i in range(NX):
        x = i * DX
        E[i] = np.exp(-0.005 * (x - center) * (x - center))
        H[i] = 0.0
    return E, H

def update_E(E, H, NX):
    for i in range(1, NX):
        E[i] = E[i] + (DT/DX) * (H[i] - H[i-1])
    E[0] = E[1]
    return E

def update_H(E, H, NX):
    for i in range(NX-1):
        H[i] = H[i] + (DT/DX) * (E[i+1] - E[i])
    H[NX-1] = H[NX-2]
    return H

def parallel_field_calc(NX, DX, NSTEPS):
    return field_calc(NX, DX, NSTEPS)

def field_calc(NX, DX, NSTEPS):
    E, H = initialize_fields(NX, DX)
    for i in range(NSTEPS):
        H = update_H(E, H, NX)
        E = update_E(E, H, NX)
    return E

def main():
    NXs=[400, 1000, 6400, 16000, 6400000]
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        print("Process started")
        results = pool.starmap(parallel_field_calc, [(NX, DX, NSTEPS) for NX in NXs])
        figure, axes = plt.subplots(len(NXs), 1, figsize=(24, 8 * len(NXs)))
    
    for idx, E in enumerate(results):
        max_idx = np.argmax(E)
        NX = NXs[idx]
        ax = axes[idx] if len(NXs) > 1 else axes
        ax.set_title(f"Electric Field (E) with Gaussian Pulse - NX={NX}")
        ax.plot(np.arange(NX) * DX, E, label=f"Electric Field (E) - NX={NX}", lw=1)
        ax.set_title(f"Electric Field (E) with Gaussian Pulse - NX={NX}, Maximum at NX={max_idx}")
        ax.set_xlabel("Position (x)")
        ax.set_ylabel("Field Strength (E)")
        ax.legend()
        ax.grid(True)
    plt.tight_layout(pad=5.0)
    plt.show()
    plt.savefig("./5_project/5_test/field_NXs.png")

if __name__ == "__main__":
    main()
