import numpy as np

def approximated_gaussian_amplitudes(n_qubits: int, R):

    dim = 2 ** n_qubits
    print(f"dim: {dim}")
    x = np.arange(dim, dtype=float)
    print(f"x: {x}")


    # amplitudes proportional to e^{-(x-mu)^2 / (2*sigma^2)}
    # amp = np.exp(-0.5 * ((x - mu) / sigma) ** 2)

    # NOWE PODEJŚCIE - DOKŁADNIE TAKA FUNKCJA JAKA JEST ZAPROPONOWANA U MIDASA:
    amp = np.exp(-1*np.pi * ((x / R) ** 2))
    print(f"np.pi: {np.pi}")

    print(f"amp: {amp}")

    # normalization to sum(|amp|^2) = 1
    norm = np.linalg.norm(amp)
    print(f"norm: {norm}")
    if norm == 0:
        raise ValueError("Zero vector: choose different mu/sigma.")
    amp = amp / norm
    print(f"amp: {amp}")
    print(f"amp**2: {amp**2}")
    print(f"sum(amp**2): {sum(amp**2)}")
    return amp


if __name__ == "__main__":
    amp = approximated_gaussian_amplitudes(4, 2)
    # print(amp)