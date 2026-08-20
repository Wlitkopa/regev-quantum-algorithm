"""Compute (mu, sigma, amps) for the Gaussian initial superposition and
apply it to the circuit.

``gauss_init`` from the user script is a two-element list where each element
can either be a concrete value or the sentinel ``False`` meaning "use the
default derived from n and R".
"""

import math
from dataclasses import dataclass
from typing import Iterable

import numpy as np

from gates.r_haner.grover_rudolph import grover_rudolph
from utils.approximated_gaussian_amplitudes import approximated_gaussian_amplitudes


@dataclass
class GaussInitParams:
    mu: float
    sigma: float
    R: float
    amps: np.ndarray


def resolve_gauss_params(gauss_init, R: float, n: int, qd: int) -> GaussInitParams:
    """Turn the raw ``gauss_init`` argument into a fully resolved parameter set."""
    if isinstance(gauss_init[0], bool):
        mu = (2 ** n - 1) / 2.0
    else:
        mu = gauss_init[0]

    if isinstance(gauss_init[1], bool):
        sigma = R / math.sqrt(2 * math.pi)
    else:
        sigma = gauss_init[1]

    amps = approximated_gaussian_amplitudes(qd, R)
    return GaussInitParams(mu=mu, sigma=sigma, R=R, amps=amps)


def apply_gaussian_init(
    circuit,
    x_qregs: Iterable,
    amps: np.ndarray,
    use_grover_rudolph: bool,
    N: int,
    n: int,
    d: int,
    qd: int,
) -> None:
    """Attach the Gaussian initial state to each input register in ``circuit``."""
    if use_grover_rudolph:
        gate = grover_rudolph(N, n, d, qd, amps)
        for qreg in x_qregs:
            circuit.append(gate, qreg)
        circuit.barrier(*x_qregs)
    else:
        # State-injection path — only works on a statevector simulator.
        for qreg in x_qregs:
            circuit.initialize(amps, qreg)
