import numpy as np

from itertools import chain

from qiskit.circuit import Gate
from qiskit import QuantumRegister, AncillaRegister, QuantumCircuit, ClassicalRegister, transpile
from qiskit.circuit.library import RYGate
import matplotlib.pyplot as plt

from gates.r_haner.constant_modulo_multiplier import controlled_constant_modulo_multiplier, \
    controlled_constant_modulo_multiplier_regs
from utils.circuit_creation import create_circuit
from utils.typing_ import QRegsSpec
from utils.approximated_gaussian_amplitudes import approximated_gaussian_amplitudes


def grover_rudolph(N: int, n: int, d: int, qd: int, amps) -> Gate:
# def grover_rudolph(N: int, n: int, d: int, qd: int, R: int):

    # circuit = QuantumCircuit(qd, qd)
    circuit = QuantumCircuit(qd, name=f"GR")

    # amps = approximated_gaussian_amplitudes(n, R)
    probs = [amp ** 2 for amp in amps]

    for i in range(qd):
        bins = 2**(i+1)
        thetas = prepare_thetas(bins, probs)

        # Number of RY gates per bin aggregation round
        thetas_len = len(thetas)

        for j in range(thetas_len):
            if thetas_len == 1:
                circuit.ry(thetas[0], 0)
            else:
                bits = f'{j:0{i}b}'
                for k in range(len(bits)):
                    if bits[k] == '0':
                        circuit.x(k)
                # print(f"i: {i}\nj: {j}")
                circuit.append(RYGate(thetas[j]).control(i), [num for num in range(i+1)])
                for k in range(len(bits)):
                    if bits[k] == '0':
                        circuit.x(k)
        # Barriers are not necessary while using a simulator, they also prevents converting circuit to the gate
        #             else:
        #                 circuit.barrier(k)
        # circuit.barrier()


    return circuit.to_gate()
    # return circuit



def prepare_thetas(bins: int, probs: list):

    number_of_thetas = bins // 2
    cur_qubits = int(np.log2(bins))
    prev_qubits = int(np.log2(number_of_thetas))
    # print(f"cur_qubits: {cur_qubits}")
    probs_bins_previous = np.array(np.array_split(probs, number_of_thetas)).sum(axis=1)
    probs_bins_current = np.array(np.array_split(probs, bins)).sum(axis=1)

    thetas = []
    for i in range(number_of_thetas):
        cur_i = 2*i
        i_bits = f'{i:0{prev_qubits}b}'
        cur_i_bits = f'{cur_i:0{cur_qubits}b}'
        # print(f"====\ni_bits: {i_bits}\ncur_i_bits: {cur_i_bits}")
        # theta = 2 * np.arccos(np.clip(np.sqrt(probs_bins_current[cur_i] / probs_bins_previous[i]), -1.0, 1.0))
        # theta = 2 * np.arccos(np.clip(np.sqrt(probs_bins_current[cur_i] / probs_bins_previous[i]), 0.0, 1.0))
        # thetas.append(theta)

        prev = probs_bins_previous[i]

        if prev == 0:
            theta = 0.0
            thetas.append(theta)

        else:
            ratio = probs_bins_current[cur_i] / prev
            theta = 2*np.arccos(np.clip(np.sqrt(ratio), 0.0, 1.0))
            thetas.append(theta)

    return thetas



def test():
    a = [2, 4, 6]
    print(a)
    print([num**2 for num in a])

    for i in range(3):

        thetas_len = 2**i

        for j in range(thetas_len):

                bits = f'{j:0{i}b}'
                print(f'bits: {bits}')
    print([num for num in range(1)])


if __name__ == "__main__":

    test()
    N = 15
    n = N.bit_count()
    d = 2
    qd = 3
    R = 5

    circuit = grover_rudolph(N, n, d, qd, R)
    # circuit.draw(output='mpl', style='iqp-dark', fold=-1)
    plt.show()



