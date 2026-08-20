"""Regev factoring algorithm — orchestrator (facade).

Public class :class:`Regev` (and its subclass :class:`~implementations.r_haner.HanerRegev`)
is what ``regev_all.py`` interacts with. The heavy lifting is split across the
:mod:`implementations.regev_parts` package:

* :mod:`.regev_parts.simulation`   — AerSimulator config, running
* :mod:`.regev_parts.classical`    — LLL / lattice classical part
* :mod:`.regev_parts.file_analyzer`— replay classical part from saved files
* :mod:`.regev_parts.drawing`      — circuit + Gaussian probability plots
* :mod:`.regev_parts.gauss`        — Gaussian initial-state helpers
* :mod:`.regev_parts.config`       — parsing of the ``meas_R_list`` flag
* :mod:`.regev_parts.paths`        — output/image directory builders
* :mod:`.regev_parts.output`       — text-report formatters

This file is deliberately kept as the "aggregator" so all entry points remain
discoverable from one place.
"""

import logging
import math
import time
from abc import ABC, abstractmethod
from decimal import getcontext
from typing import Sequence

import numpy as np
from qiskit import AncillaRegister, ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit.circuit import Instruction
from qiskit.circuit.library import QFT

from utils.calculate_R import calculate_R
from utils.convert_milliseconds import convert_milliseconds
from utils.is_prime import is_prime
from utils.regev_result import RegevResult

from .regev_parts import (
    classical,
    drawing,
    file_analyzer,
    gauss,
    output,
    paths,
    simulation,
)
from .regev_parts import (
    config as cfg_mod,
)

logger = logging.getLogger(__name__)
getcontext().prec = 1000


class Regev(ABC):
    """Abstract Regev-algorithm driver. Backend-specific gate implementations
    are supplied by concrete subclasses (see :mod:`implementations.r_haner`).
    """

    def __init__(self, shots: int, main_path_dir: str) -> None:
        self.shots = shots
        self.result = RegevResult()
        self.vectors: list = []
        self.main_path_dir = main_path_dir

    # ------------------------------------------------------------------
    # Public entry points (called from regev_all.py)
    # ------------------------------------------------------------------

    def run_all_algorithm(
        self,
        Ns: Sequence[int],
        d_qd_list: Sequence[Sequence[bool]],
        number_of_combinations: int,
        type_of_test: int,
        find_pq: bool = False,
        gauss_init=False,
        meas_R_list: Sequence = (0,),
        use_grover_rudolph: bool = True,
    ) -> int:
        for d_ceil, qd_ceil in d_qd_list:
            d_mode = cfg_mod.mode_name(d_ceil)
            qd_mode = cfg_mod.mode_name(qd_ceil)

            for N in Ns:
                for cfg in self._iter_meas_configs(meas_R_list):
                    print(f"\nN: {N}")
                    start = time.time()
                    quantum_result = self.get_vectors(
                        N,
                        d_ceil=d_ceil,
                        qd_ceil=qd_ceil,
                        gauss_init=gauss_init,
                        measure_output_register=(cfg.measure_output_register if cfg else False),
                        is_R_big=(cfg.is_R_big if cfg else False),
                        use_grover_rudolph=use_grover_rudolph,
                    )
                    classic_result = classical.run_classical_part(
                        number_of_combinations,
                        N,
                        quantum_result.n,
                        quantum_result.number_of_primes,
                        quantum_result.exp_register_width,
                        quantum_result.squared_primes,
                        quantum_result.output_data,
                        type_of_test,
                        find_pq,
                        meas_R_list,
                    )
                    exec_time = (time.time() - start) * 1000

                    print(
                        "Per cent of combinations that gives % N = 1: "
                        f"{classic_result.success_perc_mod_N_1}%"
                    )
                    print(
                        "Per cent of combinations that give p and q: "
                        f"{classic_result.success_perc_p_q}%"
                    )

                    text = output.format_all_result(
                        quantum_result, classic_result, type_of_test,
                        number_of_combinations, exec_time, find_pq,
                    )
                    dir_ = paths.all_parts_dir(
                        self.main_path_dir, d_mode, qd_mode,
                        quantum_result.n, quantum_result.gauss_R, cfg, gauss_init,
                    )
                    file_path = output.write_result(dir_, N, text)
                    print(f"All algorithm results saved in {file_path}")
        return 0

    def run_quantum_part_data_collection(
        self,
        Ns: Sequence[int],
        d_qd_list: Sequence[Sequence[bool]],
        gauss_init,
        measure_output_register: bool = False,
        meas_R_list: Sequence = (0,),
        use_grover_rudolph: bool = True,
    ) -> None:
        for d_ceil, qd_ceil in d_qd_list:
            d_mode = cfg_mod.mode_name(d_ceil)
            qd_mode = cfg_mod.mode_name(qd_ceil)

            for N in Ns:
                for cfg in self._iter_meas_configs(meas_R_list):
                    is_R_big = cfg.is_R_big if cfg else False
                    measure_out = cfg.measure_output_register if cfg else measure_output_register

                    print(f"\nN: {N}")
                    start = time.time()
                    result = self.get_vectors(
                        N, d_ceil=d_ceil, qd_ceil=qd_ceil,
                        gauss_init=gauss_init, measure_output_register=measure_out,
                        is_R_big=is_R_big, use_grover_rudolph=use_grover_rudolph,
                    )
                    exec_time = (time.time() - start) * 1000
                    text = output.format_quantum_result(result, exec_time)
                    dir_ = paths.quantum_part_dir(
                        self.main_path_dir, d_mode, qd_mode,
                        result.n, result.gauss_R, cfg, gauss_init,
                    )
                    file_path = output.write_result(dir_, N, text)
                    print(f"Quantum part results saved in {file_path}")

                    self._print_quantum_summary(result, exec_time)

    def run_file_data_analyzer(
        self,
        Ns: Sequence[int],
        d_qd_list: Sequence[Sequence[bool]],
        number_of_combinations: int,
        type_of_test_array: Sequence[int],
        meas_R_list: Sequence = (0,),
    ) -> None:
        file_analyzer.run_file_data_analyzer(
            self.main_path_dir, Ns, d_qd_list,
            number_of_combinations, type_of_test_array, meas_R_list,
        )

    def draw_quantum_circuit(
        self,
        Ns: Sequence[int],
        d_qd_list: Sequence[Sequence[bool]],
        decompose: bool = False,
        gauss_init=False,
        meas_R_list: Sequence = (0,),
        use_grover_rudolph: bool = True,
    ) -> None:
        for cfg in self._iter_meas_configs(meas_R_list):
            for d_ceil, qd_ceil in d_qd_list:
                d_mode = cfg_mod.mode_name(d_ceil)
                qd_mode = cfg_mod.mode_name(qd_ceil)
                for N in Ns:
                    circuit = self.construct_circuit(
                        N, d_ceil, qd_ceil, gauss_init=gauss_init,
                        measure_output_register=(cfg.measure_output_register if cfg else False),
                        is_R_big=(cfg.is_R_big if cfg else False),
                        use_grover_rudolph=use_grover_rudolph,
                    )
                    general_dir, decomposed_dir = paths.circuit_image_dirs(
                        self.main_path_dir, d_mode, qd_mode,
                        self.result.n, self.result.gauss_R, cfg, gauss_init,
                    )
                    reported: list[str] = []
                    if decompose:
                        f = drawing.save_circuit_image(
                            circuit, f"{decomposed_dir}/N_{N}_decomposed", decompose=True
                        )
                        reported.append(f)
                    f = drawing.save_circuit_image(circuit, f"{general_dir}/N_{N}", decompose=False)
                    reported.append(f)
                    if gauss_init:
                        # Store the Gaussian-input plots alongside the general circuit image.
                        gauss_files = drawing.draw_gaussian_probabilities(
                            self.result, general_dir, cfg,
                        )
                        reported.append(gauss_files)
                    print("Created files:\n" + "\n".join(f" - {p}" for p in reported))

    # ------------------------------------------------------------------
    # Core: circuit construction (kept here — it *is* the algorithm)
    # ------------------------------------------------------------------

    def construct_circuit(
        self,
        N: int,
        d_ceil: bool,
        qd_ceil: bool,
        semi_classical: bool = False,
        measurement: bool = True,
        gauss_init=False,
        measure_output_register: bool = False,
        is_R_big: bool = False,
        use_grover_rudolph: bool = True,
    ) -> QuantumCircuit:
        self._validate_input(N)
        n = N.bit_length()
        d = math.ceil(math.sqrt(n)) if d_ceil else math.floor(math.sqrt(n))
        qd = (math.ceil(n / d) if qd_ceil else math.floor(n / d)) + d

        amps = None
        # gauss_init == False (or None) disables the Gaussian initial state;
        # ``[False, False]`` still enables it but uses the default (mu, sigma).
        if gauss_init:
            a = self.generate_a(d, N)
            R = calculate_R(d, qd, N, n, a, is_R_big=is_R_big)
            self.result.gauss_R = R
            params = gauss.resolve_gauss_params(gauss_init, R, n, qd)
            amps = params.amps
            self.result.gauss_init_mu = gauss_init[0]
            self.result.gauss_init_sigma = gauss_init[1]
            self.result.gauss_mu = params.mu
            self.result.gauss_sigma = params.sigma
            self.result.amps = amps
            self.result.probs = amps ** 2
            self.result.probs_sum = float(np.sum(amps ** 2))

        self.result.N = N
        self.result.n = n
        self.result.d_ceil = d_ceil
        self.result.qd_ceil = qd_ceil
        self.result.number_of_primes = d
        self.result.exp_register_width = qd
        self.result.measure_output_register = measure_output_register

        return self._construct_circuit(
            N, n, measurement, d, qd, amps, measure_output_register, use_grover_rudolph
        )

    def _construct_circuit(
        self,
        N: int,
        n: int,
        measurement: bool,
        d: int,
        qd: int,
        amps,
        measure_output_register: bool,
        use_grover_rudolph: bool,
    ) -> QuantumCircuit:
        a = self.generate_a(d, N)
        self.result.squared_primes = a

        x_qregs = [QuantumRegister(qd, name=f"x{i + 1}") for i in range(d)]
        y_qreg = QuantumRegister(n, "y")
        aux_qreg = AncillaRegister(self._get_aux_register_size(n), "aux")
        circuit = QuantumCircuit(*x_qregs, y_qreg, aux_qreg, name=self._get_name(N, d))

        if isinstance(amps, np.ndarray):
            gauss.apply_gaussian_init(circuit, x_qregs, amps, use_grover_rudolph, N, n, d, qd)
        else:
            for qreg in x_qregs:
                circuit.h(qreg)

        circuit.x(y_qreg[0])

        # Modular exponentiation on each input register.
        qregs_all = circuit.qregs
        for i in range(d):
            qubits_to_pass = list(qregs_all[i]) + list(qregs_all[-2]) + list(qregs_all[-1])
            circuit.append(self._modular_exponentiation_gate(a[i], N, n, qd), qubits_to_pass)
        circuit.barrier(*qregs_all[0:d])

        qft = QFT(qd).to_gate()
        for i in range(d):
            circuit.append(qft, qregs_all[i])
        circuit.barrier()

        if measure_output_register:
            y_creg = ClassicalRegister(n, "yValue")
            circuit.add_register(y_creg)
            circuit.measure(qregs_all[-2], y_creg)

        if measurement:
            for i in range(d):
                x_creg = ClassicalRegister(qd, name=f"x{i + 1}Value")
                circuit.add_register(x_creg)
                circuit.measure(qregs_all[i], x_creg)

        return circuit

    # ------------------------------------------------------------------
    # Simulation
    # ------------------------------------------------------------------

    def get_vectors(
        self,
        N: int,
        d_ceil: bool = False,
        qd_ceil: bool = False,
        semi_classical: bool = False,
        gauss_init=False,
        measure_output_register: bool = False,
        is_R_big: bool = False,
        use_grover_rudolph: bool = True,
    ) -> RegevResult:
        print("Running quantum part")
        start = time.time()
        self._validate_input(N)

        circuit = self.construct_circuit(
            N, d_ceil, qd_ceil, semi_classical, measurement=True,
            gauss_init=gauss_init, measure_output_register=measure_output_register,
            is_R_big=is_R_big, use_grover_rudolph=use_grover_rudolph,
        )

        print(f"Kubity:             {circuit.num_qubits}")
        print(f"Kubity decompose:   {circuit.decompose().num_qubits}")
        print(f"Bity klasyczne:     {circuit.num_clbits}")
        print(f"Bramki (łącznie):   {circuit.size()}")
        print(f"Bramki decomposed:  {circuit.decompose().size()}")
        print(f"Głębokość obwodu:   {circuit.depth()}")
        print(f"Bramki 2-kubitowe:  {circuit.num_nonlocal_gates()}")

        self.result.qubits_num = circuit.num_qubits
        self.result.bits_num = circuit.num_clbits
        self.result.gates_num = circuit.size()
        self.result.gates_decomposed_num = circuit.decompose().size()
        self.result.depth = circuit.depth()
        self.result.two_qubits_gates = circuit.num_nonlocal_gates()

        aersim = simulation.build_simulator(self.shots)
        print("Max number of qubits (local qasm_simulator):", aersim.configuration().n_qubits)

        counts = simulation.run_circuit(circuit, aersim, self.shots)
        simulation.collect_counts(counts, measure_output_register, self.result, self.shots)

        self.result.quantum_exec_time = (time.time() - start) * 1000
        # Consume the accumulated result and start a fresh one for the next N.
        result, self.result = self.result, RegevResult()
        return result

    # ------------------------------------------------------------------
    # Utilities (kept here for API compatibility with the original module)
    # ------------------------------------------------------------------

    @staticmethod
    def generate_a(d: int, N: int) -> list[int]:
        """First ``d`` odd primes squared, skipping any divisor of ``N``."""
        a: list[int] = []
        num = 2
        while len(a) < d:
            if is_prime(num):
                if N % num == 0:
                    num += 1
                    continue
                a.append(int(math.pow(num, 2)))
            num += 1
        return a

    @staticmethod
    def get_factors(vect, primes, N):
        return classical.get_factors(vect, primes, N)

    @staticmethod
    def _validate_input(N: int) -> None:
        if N < 1 or N % 2 == 0:
            raise ValueError(
                f"The input N needs to be an odd integer greater than 1. Provided N = {N}."
            )

    @staticmethod
    def _parse_measurement(measurement: str, semi_classical: bool = False) -> int:
        if semi_classical:
            measurement = measurement.replace(" ", "")
        return int(measurement, base=2)

    def _iter_meas_configs(self, meas_R_list: Sequence):
        """Yield :class:`MeasRConfig` per entry, or a single ``None`` for uniform init."""
        if cfg_mod.is_uniform_init(meas_R_list):
            yield None
            return
        for entry in meas_R_list:
            yield cfg_mod.parse_meas_R_entry(entry)

    def _print_quantum_summary(self, result: RegevResult, exec_time_ms: float) -> None:
        print(f"N: {result.N}")
        print(f"n: {result.n}")
        print(f"number_of_primes: {result.number_of_primes}")
        print(f"exp_register_width: {result.exp_register_width}")
        print(f"squared_primes: {result.squared_primes}")
        print(f"output_data: {result.output_data}")
        print(f"exec_time: {exec_time_ms}ms")
        print(f"converted_time: {convert_milliseconds(exec_time_ms)}")
        print(
            f"gauss_mu: {result.gauss_mu}, gauss_sigma: {result.gauss_sigma}, "
            f"gauss_R: {result.gauss_R}"
        )
        print(f"probabilities sum: {result.probs_sum}")

    # ------------------------------------------------------------------
    # Backend-specific gate hooks (implemented by subclasses)
    # ------------------------------------------------------------------

    @abstractmethod
    def _get_aux_register_size(self, n: int) -> int: ...

    @property
    @abstractmethod
    def _prefix(self) -> str: ...

    @abstractmethod
    def _modular_exponentiation_gate(
        self, constant: int, N: int, n: int, qd: int
    ) -> Instruction: ...

    @abstractmethod
    def _modular_multiplication_gate(self, constant: int, N: int, n: int) -> Instruction: ...

    def _get_name(self, N: int, d: int) -> str:
        return f"{self._prefix} Regev(N={N}, d={d})"
