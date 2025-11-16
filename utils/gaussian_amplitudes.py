import numpy as np

def gaussian_amplitudes(n_qubits: int, mu=None, sigma=None):
    """Returns normalized amplitudes for indexes 0..2^n-1."""
    dim = 2 ** n_qubits
    # print(f"dim: {dim}")
    x = np.arange(dim, dtype=float)
    # print(f"x: {x}")
    if mu is None:
        mu = (dim - 1) / 2.0                     # mu
    if sigma is None:
        sigma = dim / 8.0                        # sigma

    print(f"mu: {mu}")
    print(f"sigma: {sigma}")

    # amplitudes proportional to e^{-(x-mu)^2 / (2*sigma^2)}
    amp = np.exp(-0.5 * ((x - mu) / sigma) ** 2)

    # print(f"amp: {amp}")

    # normalization to sum(|amp|^2) = 1
    norm = np.linalg.norm(amp)
    # print(f"norm: {norm}")
    if norm == 0:
        raise ValueError("Zero vector: choose different mu/sigma.")
    amp = amp / norm
    # print(f"amp: {amp}")
    # print(f"amp**2: {amp**2}")
    # print(f"sum(amp**2): {sum(amp**2)}")
    return amp


# gaussian_amplitudes(4)

