"""Strict Gaussian amplitudes (retained for comparison with the approximated form)."""

import numpy as np


def gaussian_amplitudes(
    n_qubits: int, mu: float | None = None, sigma: float | None = None
) -> np.ndarray:
    """Normalised amplitudes for a Gaussian over ``[0, 2^n_qubits)``.

    When ``mu`` or ``sigma`` are ``None`` the defaults ``(dim - 1)/2`` and
    ``dim/8`` are used — reasonable when no domain-specific value is available.
    """
    dim = 2 ** n_qubits
    x = np.arange(dim, dtype=float)
    if mu is None:
        mu = (dim - 1) / 2.0
    if sigma is None:
        sigma = dim / 8.0

    amp = np.exp(-0.5 * ((x - mu) / sigma) ** 2)
    norm = np.linalg.norm(amp)
    if norm == 0:
        raise ValueError("Zero vector: choose different mu/sigma.")
    return amp / norm
