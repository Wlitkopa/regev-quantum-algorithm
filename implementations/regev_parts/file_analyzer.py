"""Re-run the classical (LLL) part from an already-written quantum-part file.

Useful when the quantum simulation is expensive: the raw quantum output is
serialised to disk, and this module later reads it back and evaluates the
classical part with different ``type_of_test`` values, without recomputing
anything on the simulator.
"""

import ast
import math
import os
import time
from pathlib import Path
from random import randint
from typing import List, Optional, Sequence

from utils.convert_milliseconds import convert_milliseconds

from .classical import _reduce_and_check, compute_lattice_params
from .config import MeasRConfig, is_uniform_init, mode_name, parse_meas_R_entry
from .paths import classical_analysis_dir, find_gauss_quantum_file

_TYPE_DIR = {1: "type_1", 2: "type_2", 3: "type_3"}


def _read_header(results) -> tuple[int, int, int, int, list]:
    """Read the fixed 10-line prelude of a quantum-part output file."""
    N = n = d = dq = 0
    a_root: list = []
    for i in range(10):
        line = results.readline()
        if i == 0:
            N = int(line.split(" ")[1])
        elif i == 1:
            n = int(line.split(" ")[1])
        elif i == 4:
            d = int(line.split(":")[1][:-1])
        elif i == 5:
            dq = int(line.split(":")[1][:-1])
        elif i == 6:
            a = ast.literal_eval(line.split(":")[1])
            a_root = [int(math.sqrt(a_)) for a_ in a]
    return N, n, d, dq, a_root


def _read_vectors(results, d: int, dq: int, type_of_test: int) -> List[list]:
    vectors: List[list] = []
    total_number_of_vectors = 0
    while (line := results.readline()) != "\n":
        v = line.split(":")[1][:-2]
        duplicate = int(line.split(" ")[2])
        if type_of_test == 1:
            vectors.extend([ast.literal_eval(v)] * duplicate)
        elif type_of_test == 2:
            vectors.append(ast.literal_eval(v))
        elif type_of_test == 3:
            total_number_of_vectors += duplicate

    if type_of_test == 3:
        for _ in range(total_number_of_vectors):
            vectors.append([randint(0, 2 ** dq) for _ in range(d)])
    return vectors


def _locate_input_file(
    main_path_dir: str,
    d_mode: str,
    qd_mode: str,
    N: int,
    cfg: Optional[MeasRConfig],
) -> tuple[Optional[str], Optional[str]]:
    """Return (file_path, gauss_params_dir) or (None, None) if missing."""
    if cfg is None:
        file_name = f"output_data/{main_path_dir}/quantum_part/{d_mode}_{qd_mode}/N_{N}"
        if not os.path.exists(file_name):
            print(f"File {file_name} doesn't exists")
            return None, None
        return file_name, None

    file_name, gauss_params_dir = find_gauss_quantum_file(
        main_path_dir, d_mode, qd_mode, N, cfg
    )
    if file_name is None:
        print(f"File N_{N} not found")
    return file_name, gauss_params_dir


def analyze_one(
    main_path_dir: str,
    N: int,
    d_ceil: bool,
    qd_ceil: bool,
    number_of_combinations: int,
    type_of_test: int,
    meas_R_list: Sequence,
    cfg: Optional[MeasRConfig],
) -> None:
    d_mode = mode_name(d_ceil)
    qd_mode = mode_name(qd_ceil)

    print(f"\n================ N: {N} ================")
    print(
        "================ GAUSS ================"
        if cfg
        else "================ UNIFORM ================"
    )

    file_name, gauss_params_dir = _locate_input_file(
        main_path_dir, d_mode, qd_mode, N, cfg
    )
    if file_name is None:
        return

    with open(file_name) as results:
        N, n, d, dq, a_root = _read_header(results)
        vectors = _read_vectors(results, d, dq, type_of_test)

        if type_of_test == 2 and len(vectors) < d + 4:
            print(f"\nToo little variety of vectors for number {N}\n")
            _write_result(
                f"\nToo little variety of vectors for number {N}\n",
                main_path_dir, type_of_test, d_mode, qd_mode, cfg, gauss_params_dir, N,
            )
            return

        start = time.time()
        params = compute_lattice_params(N, n, d, meas_R_list)
        n_est = math.ceil(math.log(N, 2))

        print(
            f"Parameters:\nN: {N}\nR: {params.R}\nT: {params.T}\n"
            f"t: {params.t}\ndelta: {params.delta}\ndelta_inv: {params.delta_inv}"
        )

        header = (
            f"N: {N}\n"
            f"n: {n_est}\n"
            f"number_of_primes (d): {d}\n"
            f"exp_register_width (qd): {dq}\n"
            f"primes: {a_root}\n\n"
            f"R: {params.R}\n"
            f"T: {params.T}\n"
            f"t: {params.t}\n"
            f"delta: {params.delta}\n"
            f"delta_inv: {params.delta_inv}\n"
        )

        p_q_vectors: List = []
        success1 = success2 = 0
        for _ in range(number_of_combinations):
            s1, s2, found = _reduce_and_check(vectors, a_root, d, N, params)
            success1 += s1
            success2 += s2
            if found is not None:
                p_q_vectors.append(found)

        exec_time = (time.time() - start) * 1000
        result = (
            f"{header}"
            f"Percent of combinations that give % N = 1: "
            f"{success1 * 100 / number_of_combinations}%\n"
            f"Percent of combinations that give p and q: "
            f"{success2 * 100 / number_of_combinations}%\n"
            f"Vectors that gives p and q: {p_q_vectors}\n"
            f"\nexec_time (ms): {exec_time} ms\n"
            f"exec_time: {convert_milliseconds(exec_time)}"
        )
        print(result)

    _write_result(
        result, main_path_dir, type_of_test, d_mode, qd_mode, cfg, gauss_params_dir, N
    )


def _write_result(
    result: str,
    main_path_dir: str,
    type_of_test: int,
    d_mode: str,
    qd_mode: str,
    cfg: Optional[MeasRConfig],
    gauss_params_dir: Optional[str],
    N: int,
) -> None:
    dir_path = classical_analysis_dir(
        main_path_dir, _TYPE_DIR[type_of_test], d_mode, qd_mode, cfg, gauss_params_dir
    )
    file_path = Path(dir_path) / f"N_{N}"
    file_path.write_text(result)
    print(f"Classical part results saved in {file_path}")


def run_file_data_analyzer(
    main_path_dir: str,
    Ns: Sequence[int],
    d_qd_list: Sequence[Sequence[bool]],
    number_of_combinations: int,
    type_of_test_array: Sequence[int],
    meas_R_list: Sequence,
) -> None:
    """Iterate every (type_of_test, d_qd, meas_R, N) tuple and re-analyze it."""
    for type_of_test in type_of_test_array:
        print(f"\n\nTYPE OF TEST: {type_of_test}\n\n")
        for d_ceil, qd_ceil in d_qd_list:
            entries = [None] if is_uniform_init(meas_R_list) else [
                parse_meas_R_entry(e) for e in meas_R_list
            ]
            for cfg in entries:
                for N in Ns:
                    analyze_one(
                        main_path_dir, N, d_ceil, qd_ceil,
                        number_of_combinations, type_of_test, meas_R_list, cfg,
                    )
