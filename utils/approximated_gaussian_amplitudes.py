"""Approximated Gaussian amplitudes for the Grover-Rudolph state preparation.

Uses ``exp(-π(x/R)^2)`` (the "Midas" approximation) rather than the strict
Gaussian ``exp(-(x-mu)^2 / (2σ^2))``: the shape is close enough that the
Grover-Rudolph decomposition is well-behaved, while the analytical form is
easier to reason about in the Regev-with-Gaussian analysis.
"""

import numpy as np


def approximated_gaussian_amplitudes(n_qubits: int, R: float) -> np.ndarray:
    """Return normalised amplitudes over ``[0, 2^n_qubits)``."""
    dim = 2 ** n_qubits
    x = np.arange(dim, dtype=float)
    amp = np.exp(-np.pi * ((x / R) ** 2))

    norm = np.linalg.norm(amp)
    if norm == 0:
        raise ValueError("Zero vector: choose different R.")
    return amp / norm
