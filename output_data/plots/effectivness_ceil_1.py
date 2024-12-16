import matplotlib.pyplot as plt
import numpy as np

# quantum part

N = [15, 21, 33, 35, 39, 51, 55, 57]
regev_ceil_ceil_effectivness_1_N_1 = []
regev_floor_ceil_h = [i // 3600000 for i in regev_floor_ceil_time_ms]
regev_floor_floor_time_ms = [14698, 34719, 383576, 399456, 405097, 364752, 446004, 369373, 2199122, 2239205, 2256183,
                             2106013, 2381526, 2270617, 2260646, 43569800]
regev_floor_floor_h = [i // 3600000 for i in regev_floor_floor_time_ms]
# odejmowanie części klasycznej ze względu na zaokrąglenie do ms nie ma sensu
shor_time_ms_all = [17820, 67915, 1083631, 1097304, 1118240, 1087438, 1151647, 1139126, 32314573, 34290676, 35403319]
shor_h = [i // 3600000 for i in shor_time_ms_all]

plt.xlabel("N - factorized number")
plt.ylabel("time [h]")
plt.plot(N[:len(regev_floor_ceil_h)], regev_floor_ceil_h, label="Regev's algorithm floor_ceil")
plt.plot(N[:len(regev_floor_floor_h)], regev_floor_floor_h, label="Regev's algorithm floor_floor")
plt.plot(N[:len(shor_h)], shor_h, label="Shor's algorithm")
plt.title("Quantum computations executing time")
# plt.legend(bbox_to_anchor=(0, 0.92, 1, 0.2), loc="lower left", mode="expand", borderaxespad=0, ncol=3)
plt.subplots_adjust(bottom=0.25)
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, frameon=False)
plt.grid(color='gray', linestyle='--', linewidth=0.25)
plt.savefig("./outputs_plots/regev_floor_quantum_time.png")