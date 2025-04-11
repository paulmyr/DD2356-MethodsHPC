import numpy as np
import matplotlib.pyplot as plt
data = {1000000: 0.004609} # largest sample point for one core in N: t[s]
# datapoints above 10e7 contain other memory alloc of 200GB
# full_data = {1000: 0.000007,10000: 0.000066,100000: 0.000655,1000000: 0.004609,10000000: 0.048994, 1000000000: 3.956712, 2000000000: 12.953206, 4000000000: 25.819727, 8000000000: 54.928207} # N: t[s]
bw = 29389.9 # MB/s from stream.c
bw_add = 21497.8 
arithmetic_intensity = 1
operational_intensity = np.array([1/24 for item in data.items()])  # FLOPs per byte
performance = np.array([item[0] / item[1] *10e-9 for item in data.items()])  # GFLOP/s
bw_limit = bw * 10e-3 # [FLOPs/Byte(in np.logspace below) * MB/s * 10e-3 -> GFLOPs/s]
plt.figure(figsize=(8,6))
plt.loglog(operational_intensity, performance, marker='o', label='Measured Data')
plt.axhline(y=2.25*16, color='r', linestyle='--', label='Peak FLOP/s [GFLOP/s]') # assuming SIMD
#plt.axline((0.1, 10), slope=1, linestyle='dotted', color='gray', label='Memory Bandwidth Limit') # result of Stream.c
plt.plot(np.logspace(-3, 3) , np.logspace(-3, 3)*bw_limit, linestyle='dotted', color='b', label='Memory Bandwidth Limit') # fixed axline for plt.loglog
plt.xlabel('Operational Intensity (FLOPs/Byte)')
plt.ylabel('Performance (GFLOP/s)')
plt.title('Roofline Model')
plt.legend()
plt.grid(True, which='both', linestyle='--')
plt.show()
