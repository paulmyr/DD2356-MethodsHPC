import numpy as np
import matplotlib.pyplot as plt
# replace with actual data
message_sizes = np.array([4, 8, 16, 32, 64, 128, 256, 512, 1204, 2048, 4096])  # in Bytes
rtt_times = np.array([3277.695000, 7.003000, 21.010000, 1.062000, 0.831000, 0.762000, 0.902000, 1.513000, 0.842000, 0.852000, 2.765000])  # in microseconds

coeffs = np.polyfit(message_sizes, rtt_times, 1)
latency_extrapolated = coeffs[1]  # y-intercept

plt.plot(message_sizes, rtt_times, 'o', label='Measured RTT')
plt.plot(message_sizes, coeffs[0]*message_sizes + coeffs[1], '--', label='Linear Fit')
plt.xlabel('Message Size (Bytes)')
plt.ylabel('Round-Trip Time (microseconds)')
plt.title(f'Extrapolated Latency at Zero Message Size: {latency_extrapolated:.2f} µs')
plt.legend()
plt.show()
