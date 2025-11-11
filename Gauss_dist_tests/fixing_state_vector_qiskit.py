from operator import truediv
from typing import Union, Tuple, Optional

import numpy as np
from abc import ABC, abstractmethod
from itertools import chain, combinations

from qiskit import QuantumRegister, AncillaRegister, QuantumCircuit, ClassicalRegister, transpile
from qiskit.visualization import plot_state_city, plot_bloch_multivector
from qiskit.quantum_info import Statevector

from qiskit.circuit import Instruction
from qiskit.circuit.library import QFT
from qiskit.visualization.circuit import matplotlib

from utils.circuit_creation import create_circuit
from utils.is_prime import is_prime
from utils.convert_measurement import convert_measurement
from utils.convert_to_matrix_row import convert_to_matrix_row
from utils.convert_milliseconds import convert_milliseconds

import logging
import math
import olll
from random import shuffle, randint
from fractions import Fraction
from decimal import Decimal, getcontext
import time
# from utils.secrets import ibm_api_token

import os
import ast
import math
import olll
import itertools
import matplotlib.pyplot as plt
from qiskit.providers import  Backend
from qiskit_aer import AerSimulator
# from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
# from qiskit_ibm_runtime import SamplerV2 as Sampler

#from qiskit.utils.validation import validate_min

# qubits
# n = 5
# shots = 1000
# #
# qc = QuantumCircuit(n)
# qc.h(0)
# qc.h(1)
# qc.h(2)
# qc.h(3)
# qc.h(4)

def gaussian_amplitudes(n_qubits: int, mu=None, sigma=None):
    """Zwraca znormalizowane amplitudy Gaussa po indeksach 0..2^n-1."""
    dim = 2 ** n_qubits
    x = np.arange(dim, dtype=float)
    if mu is None:
        mu = (dim - 1) / 2.0                     # środek
    if sigma is None:
        sigma = dim / 8.0                        # domyślna "szerokość"

    # amplitudy proporcjonalne do e^{-(x-mu)^2 / (2*sigma^2)}
    amp = np.exp(-0.5 * ((x - mu) / sigma) ** 2)

    # normalizacja do sum(|amp|^2) = 1
    norm = np.linalg.norm(amp)
    if norm == 0:
        raise ValueError("Zero vector: dobierz inne mu/sigma.")
    amp = amp / norm
    return amp.astype(complex)


# PARAMS
N = 21
a = [4, 25, 121]
d = 2
qd = 3
n = d*qd
mu = 0
sigma = None

# n = N.bit_length()
print(f"n: {n}")
d_ceil = True
qd_ceil = True
a_root = []

start = time.time()

for a_ in a:
    a_root.append(int(math.sqrt(a_)))



# if d_ceil:
#     d = math.ceil(math.sqrt(n))
# else:
#     d = math.floor(math.sqrt(n))
#
# if qd_ceil:
#     qd = math.ceil(n / d) + d
# else:
#     qd = math.floor(n / d) + d


m = math.ceil(n / d) + 2
powers = []
for i in range(m):
    powers.append(i)

T = N

for p in itertools.product(powers, repeat=d):
    if p == (0,) * d:
        continue
    T_tmp = 1
    v_len_tmp = 1
    for i in range(d):
        T_tmp *= pow(a_root[i], p[i], N)
        v_len_tmp += pow(p[i], 2)
    v_len_tmp = math.ceil(math.sqrt(v_len_tmp))
    if T_tmp % N == 1 and v_len_tmp < T:
        T = v_len_tmp

# R = math.ceil(6 * T * math.sqrt((d + 5) * (2 * d + 4) * (d / 2)) * (2 ** ((n + 1) / (d + 4) + d + 2)))
# print(f"R: {R}")
# sigma = R/math.sqrt(2*math.pi)
print(f"sigma: {sigma}")

# 1) amplitudy Gaussa
amps = gaussian_amplitudes(qd, mu=mu, sigma=sigma)

# 2) obwód i inicjalizacja (bez pomiarów)
qc = QuantumCircuit(n)
print([j for j in range(0, 3)])
print([j for j in range(3, 6)])
print(type(range(0,3)))
for i in range(d):
    st = i*qd
    en = st + qd
    print(st, en)
    qc.initialize(amps, [j for j in range(st, en)])   # przygotuj stan |psi> o danych amplitudach

# qc.draw(output='mpl', filename=f'/home/koan/myHome/AGH/PracaMagisterska/praca_magisterska_kod/regev-quantum-algorithm/Gauss_dist_tests/circuits/test.png', style='iqp-dark', fold=-1)

qc.save_statevector()
qc.draw(output='mpl', filename=f'/home/koan/myHome/AGH/PracaMagisterska/praca_magisterska_kod/regev-quantum-algorithm/Gauss_dist_tests/circuits/test.png', style='iqp-dark', fold=-1)

# 3) symulator statevector (bez pomiaru)
sim = AerSimulator(method="statevector")
pm = transpile(qc, sim)
res = sim.run(pm).result()

# 4) wektor stanu i prawdopodobieństwa
state = res.get_statevector(pm)                # amplitudy złożone (complex)
probs = np.abs(np.array(state))**2
print(f"state_vector: {state}")
print(f"probs: {probs}")

print(f"probs sum: ", np.sum(probs))

states = [format(i, f"0{n}b") for i in range(len(probs))]

plt.figure(figsize=(8,4))
plt.bar(states, probs)
plt.xlabel("Stan bazowy |k⟩")
plt.ylabel("Prawdopodobieństwo |αₖ|²")
plt.title("Rozkład amplitud (prawdopodobieństwa pomiaru)")
plt.savefig("/home/koan/myHome/AGH/PracaMagisterska/praca_magisterska_kod/regev-quantum-algorithm/Gauss_dist_tests/plots/statevector_probs.png", dpi=300, bbox_inches='tight')


# plt.figure(figsize=(8,4))
# plt.bar(states, np.real(amps), label="Re(αₖ)", alpha=0.7)
# plt.bar(states, np.imag(amps), label="Im(αₖ)", alpha=0.7)
# plt.legend()
# plt.title("Części rzeczywiste i urojone amplitud")
# plt.savefig("/home/koan/myHome/AGH/PracaMagisterska/praca_magisterska_kod/regev-quantum-algorithm/Gauss_dist_tests/plots/statevector_real_imag.png", dpi=300, bbox_inches='tight')
# plt.close()


# plt.figure(figsize=(8,4))
# plt.bar(states, np.angle(amps))
# plt.title("Fazy amplitud")
# plt.xlabel("Stan bazowy |k⟩")
# plt.ylabel("Faza (radiany)")
# plt.savefig("/home/koan/myHome/AGH/PracaMagisterska/praca_magisterska_kod/regev-quantum-algorithm/Gauss_dist_tests/plots/statevector_phases.png", dpi=300, bbox_inches='tight')
# plt.close()

# sv = Statevector.from_instruction(qc)
# fig1 = plot_state_city(sv, title="Reprezentacja statevectora")
# fig1.savefig("/home/koan/myHome/AGH/PracaMagisterska/praca_magisterska_kod/regev-quantum-algorithm/Gauss_dist_tests/plots/state_city.png", dpi=300, bbox_inches='tight')
#
# fig2 = plot_bloch_multivector(sv)
# fig2.savefig("/home/koan/myHome/AGH/PracaMagisterska/praca_magisterska_kod/regev-quantum-algorithm/Gauss_dist_tests/plots/state_bloch.png", dpi=300, bbox_inches='tight')

plt.plot(np.abs(amps)**2)
plt.xlabel("Indeks bazowy")
plt.ylabel("|αₖ|²")
plt.title("Rozkład Gaussa w stanie kwantowym")
plt.savefig("/home/koan/myHome/AGH/PracaMagisterska/praca_magisterska_kod/regev-quantum-algorithm/Gauss_dist_tests/plots/gaussian_distribution.png", dpi=300, bbox_inches='tight')
plt.close()




exit(0)


aersim = AerSimulator(method="statevector")
pm = transpile(qc, aersim)
result = aersim.run(pm).result()
print(f"result: {result}")

state = result.get_statevector(pm)
print(f"state: {state}")

qc.draw(output='mpl', filename=f'/home/koan/myHome/AGH/PracaMagisterska/praca_magisterska_kod/regev-quantum-algorithm/Gauss_dist_tests/circuits/test.png', style='iqp-dark', fold=-1)

# print(f"state_vector: {state_vector}")
exit(0)
