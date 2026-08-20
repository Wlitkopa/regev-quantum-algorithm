#!/usr/bin/env python3
"""Legacy Shor-order-finding driver kept for parity with the original repo.

Not part of the Regev-with-Gaussian pipeline; use :mod:`regev_all` for that.
"""

import os
import time

from implementations.haner import HanerShor as Shor
from utils.convert_milliseconds import convert_milliseconds
from utils.convert_to_orders_list import convert_to_order_list
from utils.get_coprime import (
    first_primes_list,
    get_low_level_prime,
    is_miller_rabin_passed,
)

Ns = [55]


def _pick_a(N: int, n: int, tries: int = 50) -> int:
    """Find some ``a`` coprime with ``N`` — Miller-Rabin first, sieve fallback."""
    for _ in range(tries):
        pc = get_low_level_prime(n, N)
        if is_miller_rabin_passed(pc) and pc < N and N % pc != 0:
            return pc
    for candidate in reversed(first_primes_list):
        if candidate < N and N % candidate != 0:
            return candidate
    return 1


def main() -> None:
    for N in Ns:
        n = N.bit_length()
        print(f"\nN: {N}")
        start = time.time()

        a = _pick_a(N, n)
        print(f"picked a: {a}")

        # Explicit a = 13 kept from the original script for reproducibility
        # of the recorded results; remove this line to use the sampled `a`.
        a = 13

        shor = Shor(shots=128)
        shor.construct_circuit(a, N, semi_classical=False, measurement=True)
        result = shor.get_order(a, N, semi_classical=False)

        exec_time = (time.time() - start) * 1000
        orders = convert_to_order_list(result.all_orders)

        result_str = (
            f"N: {result.N}\n"
            f"n: {result.n}\n"
            f"random a: {result.random_prime}\n"
            f"total_shots: {result.total_shots}\n"
            f"successful_shots: {result.successful_shots}\n"
            f"total results count: {result.total_counts}\n"
            f"successful results count: {result.successful_counts}\n"
            f"output_data: {result.output_data}\n"
            f"\nall orders: {orders}\n"
            f"\norder: {result.order}\n"
            f"\naverage classical part exec time (ms): {result.classical_milliseconds}\n"
            f"average classical part exec time: "
            f"{convert_milliseconds(result.classical_milliseconds)}\n"
            f"\nexec_time (ms): {exec_time} ms\n"
            f"exec_time: {convert_milliseconds(exec_time)}"
        )
        os.makedirs(f"output_data/shor/N_{N}", exist_ok=True)
        with open(f"output_data/shor/N_{N}/a_{a}", "w") as file:
            file.write(result_str)
        print(result_str)


if __name__ == "__main__":
    main()
