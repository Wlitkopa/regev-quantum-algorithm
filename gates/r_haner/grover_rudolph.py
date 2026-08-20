"""Grover-Rudolph state preparation gate.

Given a target probability distribution encoded in ``amps``, iteratively
partitions the ``qd``-qubit register in binary bins and applies a controlled
RY rotation on each so that the final statevector has amplitudes ``amps``.
Complexity is ``O(2^qd)`` gates in the worst case; sufficient for the small
``qd`` values used in the thesis experiments.

Reference:
    Grover, L. & Rudolph, T. — "Creating superpositions that correspond to
    efficiently integrable probability distributions" (2002).
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Gate
from qiskit.circuit.library import RYGate


def grover_rudolph(N: int, n: int, d: int, qd: int, amps) -> Gate:
    """Return a ``qd``-qubit gate that prepares the amplitudes ``amps``."""
    circuit = QuantumCircuit(qd, name="GR")
    probs = [amp ** 2 for amp in amps]

    for i in range(qd):
        bins = 2 ** (i + 1)
        thetas = prepare_thetas(bins, probs)

        for j, theta in enumerate(thetas):
            if len(thetas) == 1:
                circuit.ry(theta, 0)
                continue

            # Bit pattern of j sets which controls should be conjugated by X.
            bits = f"{j:0{i}b}"
            for k, bit in enumerate(bits):
                if bit == "0":
                    circuit.x(k)
            circuit.append(RYGate(theta).control(i), list(range(i + 1)))
            for k, bit in enumerate(bits):
                if bit == "0":
                    circuit.x(k)

    return circuit.to_gate()


def prepare_thetas(bins: int, probs: list) -> list:
    """RY angles for one round of bin subdivision.

    At round ``i`` the register represents ``bins/2`` current bins that are
    being split into ``bins`` finer bins; each parent bin contributes one
    rotation whose angle balances the two children.
    """
    number_of_thetas = bins // 2
    probs_bins_previous = np.array(np.array_split(probs, number_of_thetas)).sum(axis=1)
    probs_bins_current = np.array(np.array_split(probs, bins)).sum(axis=1)

    thetas: list = []
    for i in range(number_of_thetas):
        prev = probs_bins_previous[i]
        if prev == 0:
            thetas.append(0.0)
            continue
        ratio = probs_bins_current[2 * i] / prev
        thetas.append(2 * np.arccos(np.clip(np.sqrt(ratio), 0.0, 1.0)))

    return thetas
