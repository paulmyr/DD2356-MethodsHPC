import numpy as np
import matplotlib.pyplot as plt
#{'aggregate.txt': [], 'exercise2_3.txt': ['Execution time: 0.004609 seconds, N: 1000000'], 'exercise2_5.txt': [], 'exercise2_0.txt': ['Execution time: 0.000007 seconds, N: 1000'], 'exercise2_2.txt': ['Execution time: 0.000655 seconds, N: 100000'], 'exercise2_4.txt': ['Execution time: 0.048994 seconds, N: 10000000'], 'exercise2_1.txt': ['Execution time: 0.000066 seconds, N: 10000']}
data = {1000: 0.000007,10000: 0.000066,100000: 0.000655,1000000: 0.004609,10000000: 0.048994, 1000000000: 3.956712, 2000000000: 12.953206, 4000000000: 25.819727, 8000000000: 54.928207} # N: t[s]

bw = 21497.8 # MB/s from stream.c
operational_intensity = np.array([item[0]/24 for item in data.items()])  # FLOPs per byte
performance = np.array([item[0] / item[1] *10e-9 for item in data.items()])  # GFLOP/s
bw_limit = operational_intensity * bw * 10e-3 #[FLOPs/Byte * MB/s * 10e-3 -> GFLOPs/Byte]
plt.figure(figsize=(8,6))
plt.loglog(operational_intensity, performance, marker='o', label='Measured Data')
plt.axhline(y=2.25*16, color='r', linestyle='--', label='Peak FLOP/s [GFLOP/s]')
#plt.axline((0.1, 10), slope=1, linestyle='dotted', color='gray', label='Memory Bandwidth Limit') # result of Stream.c
plt.plot(operational_intensity, bw_limit, linestyle='dotted', color='gray', label='Memory Bandwidth Limit')
plt.xlabel('Operational Intensity (FLOPs/Byte)')
plt.ylabel('Performance (GFLOP/s)')
plt.title('Roofline Model')
plt.legend()
plt.grid(True, which='both', linestyle='--')
plt.show()
