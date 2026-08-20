from dataclasses import dataclass, field
from typing import Any, List, Optional


@dataclass
class RegevResult:
    """Container for all measured/derived quantities from one Regev run."""

    # Measurement statistics
    order: Optional[int] = None
    total_counts: int = 0
    successful_counts: int = 0
    total_shots: int = 0
    successful_shots: int = 0

    # Problem parameters
    N: int = 0
    n: int = 0
    d_ceil: bool = False
    qd_ceil: bool = False
    number_of_primes: int = 0
    exp_register_width: int = 0
    squared_primes: List[int] = field(default_factory=list)

    # Quantum measurement output
    output_data: List[Any] = field(default_factory=list)
    output_data_original: List[Any] = field(default_factory=list)
    vectors: List[Any] = field(default_factory=list)
    quantum_exec_time: float = 0.0
    measure_output_register: bool = False

    # Circuit statistics
    qubits_num: int = 0
    bits_num: int = 0
    gates_num: int = 0
    gates_decomposed_num: int = 0
    depth: int = 0
    two_qubits_gates: int = 0

    # Classical (LLL) results
    R: float = 0
    T: int = 0
    t: int = 0
    delta: float = 0
    delta_inv: int = 0
    vector: Any = 0
    p: int = 0
    q: int = 0
    classical_exec_time: float = 0.0
    success_perc_mod_N_1: float = 0
    success_perc_p_q: float = 0
    p_q_vectors: List[Any] = field(default_factory=list)

    # Gaussian initialisation
    gauss_init_mu: Any = 0
    gauss_init_sigma: Any = 0
    gauss_R: float = 0
    gauss_mu: float = 0
    gauss_sigma: float = 0
    amps: Any = field(default_factory=list)

    # Statevector-based diagnostics (only populated when statevector is requested)
    state: Any = field(default_factory=list)
    probs: Any = field(default_factory=list)
    probs_sum: float = 0
