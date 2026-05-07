from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit
import time

qc = QuantumCircuit(25)
qc.h(range(25))
qc.measure_all()

print(AerSimulator().available_devices())


sim = AerSimulator(device='CPU', precision='single')
t = time.time()
sim.run(qc, shots=1024).result()
print(f"'CPU': {time.time()-t:.2f}s")

# Bez cuQuantum
sim = AerSimulator(device='GPU', cuStateVec_enable=False, precision='single')
t = time.time()
sim.run(qc, shots=100).result()
t_bez = time.time() - t

# Z cuQuantum
sim_cq = AerSimulator(device='GPU', cuStateVec_enable=True, precision='single')
t = time.time()
sim_cq.run(qc, shots=100).result()
t_cq = time.time() - t

print(f"GPU bez cuQuantum: {t_bez:.2f}s")
print(f"GPU z cuQuantum:   {t_cq:.2f}s")