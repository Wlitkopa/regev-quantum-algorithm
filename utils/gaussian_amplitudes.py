import numpy as np

def gaussian_amplitudes(n_qubits: int, mu=None, sigma=None):
    """Returns normalized amplitudes for indexes 0..2^n-1."""
    dim = 2 ** n_qubits
    x = np.arange(dim, dtype=float)
    if mu is None:
        mu = (dim - 1) / 2.0                     # mu
    if sigma is None:
        sigma = dim / 8.0                        # sigma

    # amplitudes proportional to e^{-(x-mu)^2 / (2*sigma^2)}
    amp = np.exp(-0.5 * ((x - mu) / sigma) ** 2)

    # normalization to sum(|amp|^2) = 1
    norm = np.linalg.norm(amp)
    if norm == 0:
        raise ValueError("Zero vector: choose different mu/sigma.")
    amp = amp / norm
    return amp.astype(complex)
