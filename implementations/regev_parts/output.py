"""Format ``RegevResult`` values into the plain-text reports written to disk.

Kept separate from the running code so the (large) f-strings do not clutter
the orchestrator.
"""

from pathlib import Path

from utils.convert_milliseconds import convert_milliseconds
from utils.convert_to_matrix_row import convert_to_matrix_row
from utils.regev_result import RegevResult


def format_quantum_result(result: RegevResult, exec_time_ms: float) -> str:
    """The full per-run summary written by :func:`run_quantum_part_data_collection`."""
    vectors = convert_to_matrix_row(result.output_data)
    converted = convert_milliseconds(exec_time_ms)
    return (
        f"N: {result.N}\n"
        f"n: {result.n}\n"
        f"d_ceil: {result.d_ceil}\n"
        f"qd_ceil: {result.qd_ceil}\n"
        f"number_of_primes (d): {result.number_of_primes}\n"
        f"exp_register_width (qd): {result.exp_register_width}\n"
        f"squared_primes: {result.squared_primes}\n"
        f"output_data: {result.output_data}\n"
        f"\nvectors: {vectors}\n"
        f"\nexec_time (ms): {exec_time_ms} ms\n"
        f"\nexec_time: {converted}\n"
        f"\nqubits_num: {result.qubits_num}\n"
        f"bits_num: {result.bits_num}\n"
        f"gates_num: {result.gates_num}\n"
        f"gates_decomposed_num: {result.gates_decomposed_num}\n"
        f"depth: {result.depth}\n"
        f"two_qubits_gates: {result.two_qubits_gates}\n"
        f"\noutput register measured: {result.measure_output_register}\n"
        f"original output data: {result.output_data_original}\n"
        f"\ngauss_init_mu: {result.gauss_init_mu}\n"
        f"gauss_init_sigma: {result.gauss_init_sigma}\n"
        f"gauss_R: {result.gauss_R}\n"
        f"gauss_mu: {result.gauss_mu}\n"
        f"gauss_sigma: {result.gauss_sigma}\n"
        f"amps: {result.amps}\n\n"
        f"\nstatevector: {result.state}\n"
        f"probabilities: {result.probs}\n"
        f"sum of probabilities: {result.probs_sum}"
    )


def format_all_result(
    quantum_result: RegevResult,
    classic_result: RegevResult,
    type_of_test: int,
    number_of_combinations: int,
    exec_time_ms: float,
    find_pq: bool,
) -> str:
    """Combined report written by :func:`run_all_algorithm`."""
    parts: list[str] = ["=============== QUANTUM PART ===============\n"]
    parts.append(
        f"N: {quantum_result.N}\n"
        f"n: {quantum_result.n}\n"
        f"d_ceil: {quantum_result.d_ceil}\n"
        f"qd_ceil: {quantum_result.qd_ceil}\n"
        f"number_of_primes (d): {quantum_result.number_of_primes}\n"
        f"exp_register_width (qd): {quantum_result.exp_register_width}\n"
        f"squared_primes: {quantum_result.squared_primes}\n"
        f"output_data: {quantum_result.output_data}\n"
        f"\nvectors: {quantum_result}\n"
        f"\nquantum part exec_time (ms): {quantum_result.quantum_exec_time}ms\n"
        f"quantum part exec_time: {convert_milliseconds(quantum_result.quantum_exec_time)}\n"
        f"\nqubits_num: {quantum_result.qubits_num}\n"
        f"bits_num: {quantum_result.bits_num}\n"
        f"gates_num: {quantum_result.gates_num}\n"
        f"gates_decomposed_num: {quantum_result.gates_decomposed_num}\n"
        f"depth: {quantum_result.depth}\n"
        f"two_qubits_gates: {quantum_result.two_qubits_gates}\n"
        f"\noutput register measured: {quantum_result.measure_output_register}\n"
        f"original output data: {quantum_result.output_data_original}\n"
        f"\ngauss_init_mu: {quantum_result.gauss_init_mu}\n"
        f"gauss_init_sigma: {quantum_result.gauss_init_sigma}"
        f"gauss_R: {quantum_result.gauss_R}\n"
        f"gauss_mu: {quantum_result.gauss_mu}\n"
        f"gauss_sigma: {quantum_result.gauss_sigma}\n"
        f"\namps: {quantum_result.amps}\n\n"
        f"statevector: {quantum_result.state}\n"
        f"probabilities: {quantum_result.probs}\n"
        f"sum of probabilities: {quantum_result.probs_sum}\n"
    )

    parts.append("\n=============== CLASSICAL PART ===============\n")
    parts.append(
        f"R: {classic_result.R}\n"
        f"T: {classic_result.T}\n"
        f"t: {classic_result.t}\n"
        f"delta: {classic_result.delta}\n"
        f"delta_inv: {classic_result.delta_inv}\n"
        f"type_of_test: {type_of_test}\n"
        f"number_of_combinations: {number_of_combinations}\n"
        f"\nPer cent of combinations that gives % N = 1: "
        f"{classic_result.success_perc_mod_N_1}%\n"
        f"Per cent of combinations that give p and q: "
        f"{classic_result.success_perc_p_q}%\n"
        f"Vectors that gives p and q: {classic_result.p_q_vectors}"
        f"\nclassical part exec_time (ms): {classic_result.classical_exec_time}ms\n"
        f"classical part exec_time: "
        f"{convert_milliseconds(classic_result.classical_exec_time)}\n"
    )

    parts.append("\n=============== ALL TOGETHER ===============\n")
    if find_pq:
        parts.append(f"p: {classic_result.p}\nq: {classic_result.q}\n")
    parts.append(
        f"total exec_time (ms): {exec_time_ms}ms\n"
        f"total exec_time: {convert_milliseconds(exec_time_ms)}"
    )
    return "".join(parts)


def write_result(directory: str, N: int, content: str) -> str:
    """Create ``directory`` if needed, write ``content`` to ``N_<N>``, return path."""
    Path(directory).mkdir(parents=True, exist_ok=True)
    file = Path(directory) / f"N_{N}"
    file.write_text(content)
    return str(file)
