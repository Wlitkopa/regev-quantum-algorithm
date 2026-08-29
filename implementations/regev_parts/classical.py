"""Classical (lattice / LLL) part of Regev's algorithm.

Once the quantum step has produced enough vectors, ``run_classical_part``
picks ``d + 4`` of them, builds the Regev lattice, LLL-reduces it and checks
whether any of the reduced basis vectors reveal a non-trivial factor of N.
"""

import math
import time
from dataclasses import dataclass
from random import randint, shuffle
from typing import List, Optional, Sequence

import numpy as np
import olll

from utils.regev_result import RegevResult

from .config import is_uniform_init


@dataclass
class LatticeParams:
    R: float
    T: int
    t: int
    delta: float
    delta_inv: int


def compute_lattice_params(
    N: int, n: int, d: int, meas_R_list: Sequence
) -> LatticeParams:
    """Estimate R, T, t, delta following the Regev / Regev-with-Gaussian variants.

    R has two variants under Gaussian init:

    * "big"   — the classical bound R = ⌈6·T·√((d+5)(2d+4)(d/2))·2^((n+1)/(d+4)+d+2)⌉
    * "small" — the tighter empirical R = √(2d)+1
    """
    T = math.ceil(math.exp(n / (2 * d)))
    n_est = math.ceil(math.log(N, 2))

    if not is_uniform_init(meas_R_list) and not meas_R_list[0][1]:
        R = math.sqrt(2 * d) + 1
    else:
        R = math.ceil(
            6 * T * math.sqrt((d + 5) * (2 * d + 4) * (d / 2))
            * (2 ** ((n_est + 1) / (d + 4) + d + 2))
        )

    t = 1 + math.ceil(math.log(math.sqrt(d) * R, 2))
    delta = math.sqrt(d / 2) / R
    delta_inv = math.ceil(R / math.sqrt(d / 2))
    return LatticeParams(R=R, T=T, t=t, delta=delta, delta_inv=delta_inv)


def build_vectors(
    output_data, d: int, qd: int, type_of_test: int
) -> Optional[List]:
    """Build the vector pool used for random sampling into the lattice.

    Types come from the thesis:
      1 — sample real quantum-produced vectors with replication weights
      2 — sample each distinct vector at most once (ignore replication)
      3 — generate uniformly random vectors, using only the total-shot count
    """
    vectors: List = []
    total_random_needed = 0
    for entry in output_data:
        duplicate = entry[2]
        if type_of_test == 1:
            for _ in range(min(d + 4, duplicate)):
                vectors.append(entry[0])
        elif type_of_test == 2:
            vectors.append(entry[0])
        elif type_of_test == 3:
            total_random_needed += duplicate

    if type_of_test == 3:
        for _ in range(total_random_needed):
            vectors.append([randint(0, 2 ** qd) for _ in range(d)])

    if type_of_test == 2 and len(vectors) < d + 4:
        return None
    return vectors


def _reduce_and_check(
    vectors, a_root, d: int, N: int, params: LatticeParams
) -> tuple[int, int, Optional[List]]:
    """One LLL reduction on a random ``d+4``-vector sample.

    Returns ``(s1, s2, found_vector)`` where ``s1`` = 1 iff the lattice produced
    an element that squares to 1 modulo N, ``s2`` = 1 iff that element is a
    non-trivial square root of 1 (and therefore reveals a factor).
    """
    shuffle(vectors)
    w = vectors[: d + 4]

    I_d = np.identity(d)
    zeros_d_d4 = np.zeros((d, d + 4))
    I_d4_d4_delta = params.delta_inv * np.identity(d + 4)

    M = np.block([
        [I_d, zeros_d_d4],
        [np.matrix(w) * (params.delta_inv / (2 ** params.t)), I_d4_d4_delta],
    ])
    np.set_printoptions(precision=6, suppress=True)

    M_LLL = olll.reduction(M.transpose().tolist(), 0.75)
    M_LLL_t = np.matrix(M_LLL).transpose().tolist()

    for i in range(0, 2 * d + 4):
        square = 1
        temp_vector: List = []
        for j in range(d):
            square = (square * pow(a_root[j], M_LLL_t[i][j], N)) % N
            temp_vector.append(M_LLL_t[i][j])
        if (square * square) % N == 1 and temp_vector != d * [0]:
            if square != N - 1 and square != 1:
                return 1, 1, temp_vector
            return 1, 0, None
    return 0, 0, None


def run_classical_part(
    number_of_combinations: int,
    N: int,
    n: int,
    d: int,
    qd: int,
    a: Sequence[int],
    output_data,
    type_of_test: int,
    find_pq: bool = False,
    meas_R_list: Sequence = (0,),
) -> Optional[RegevResult]:
    """Return a populated :class:`RegevResult`, or ``None`` if the quantum step
    did not produce enough distinct vectors to run the lattice reduction.
    """
    result = RegevResult()
    a_root = [int(math.sqrt(a_)) for a_ in a]

    vectors = build_vectors(output_data, d, qd, type_of_test)
    if vectors is None:
        print(f"\nToo little variety of vectors for number {N}\n")
        return None

    start = time.time()
    params = compute_lattice_params(N, n, d, meas_R_list)
    print(
        f"Parameters:\nN: {N}\nR: {params.R}\nT: {params.T}\n"
        f"t: {params.t}\ndelta: {params.delta}\ndelta_inv: {params.delta_inv}"
    )

    result.R = params.R
    result.T = params.T
    result.t = params.t
    result.delta = params.delta
    result.delta_inv = params.delta_inv

    p_q_vectors: List = []
    success1 = success2 = 0
    for _ in range(number_of_combinations):
        s1, s2, found = _reduce_and_check(vectors, a_root, d, N, params)
        if s1:
            success1 += 1
        if s2:
            success2 += 1
        if found is not None:
            p_q_vectors.append(found)

    result.classical_exec_time = (time.time() - start) * 1000

    if p_q_vectors:
        result.vector = p_q_vectors[0]
    result.p_q_vectors = p_q_vectors
    result.success_perc_mod_N_1 = success1 * 100 / number_of_combinations
    result.success_perc_p_q = success2 * 100 / number_of_combinations
    print(f"p_q_vectors: {p_q_vectors}")
    print(f"Per cent of combinations that give % N = 1: {result.success_perc_mod_N_1}%")
    print(f"Per cent of combinations that give p and q: {result.success_perc_p_q}%")

    if find_pq and p_q_vectors:
        p, q = get_factors(p_q_vectors[0], a_root, N)
        result.p = p
        result.q = q

    return result


def get_factors(vect, primes, N):
    """Trivial Chinese-Remainder-style extraction of the factors from a
    non-trivial square root of 1 (mod N).
    """
    print("Calculating p and q")
    prod = 1
    for i, prime in enumerate(primes):
        prod = (prod * pow(prime, vect[i], N)) % N

    val2 = prod + 1
    p = math.gcd(int(val2), N)
    if p == N:
        print(f"We've got bad luck number one - p and q are both dividers of ({val2} + 1)")
        return -1
    if p == 1:
        print(f"We've got bad luck number two - p and q are both dividers of ({val2} - 1)")
        return -1

    q = int(N / p)
    print(f"p: {p}\nq: {q}")
    return p, q
