from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit
import time

# Sprawdź dostępne urządzenia
sim = AerSimulator()
print("Dostępne urządzenia:", sim.available_devices())

# Mały benchmark
qc = QuantumCircuit(20)
qc.h(range(20))
qc.measure_all()

for device in ['CPU', 'GPU']:
    sim = AerSimulator(device=device, precision='single')
    t = time.time()
    sim.run(qc, shots=1024).result()
    print(f"{device}: {time.time()-t:.2f}s")

print(AerSimulator().available_devices())