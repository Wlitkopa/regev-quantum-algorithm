"""Compute the R parameter used both in the classical lattice step and to
shape the Gaussian initial superposition.

Two flavours:

* ``is_R_big=True``  — exact R derived from the actual smallest T (expensive
  when d or n are large, requires enumerating powers).
* ``is_R_big=False`` — tighter empirical R = √(2d) + 1, matching what is
  reported in the thesis for the "small R" variant.
"""

import itertools
import math


def calculate_R(d: int, qd: int, N: int, n: int, a, is_R_big: bool = False) -> float:
    if not is_R_big:
        return math.sqrt(2 * d) + 1

    a_root = [int(math.sqrt(a_)) for a_ in a]
    m = math.ceil(n / d) + 2
    powers = list(range(m))

    T = N
    for p in itertools.product(powers, repeat=d):
        if p == (0,) * d:
            continue
        T_tmp = 1
        v_len_tmp = 1
        for i in range(d):
            T_tmp *= pow(a_root[i], p[i], N)
            v_len_tmp += pow(p[i], 2)
        v_len_tmp = math.ceil(math.sqrt(v_len_tmp))
        if T_tmp % N == 1 and v_len_tmp < T:
            T = v_len_tmp

    return math.ceil(
        6 * T * math.sqrt((d + 5) * (2 * d + 4) * (d / 2))
        * (2 ** ((n + 1) / (d + 4) + d + 2))
    )
