from implementations.haner import HanerShor as Shor # (big size of circuit!)
from utils.convert_milliseconds import convert_milliseconds
from utils.convert_to_orders_list import convert_to_order_list
from utils.get_coprime import *
import time
import os

# Ns = [15, 21, 33, 35, 39, 51, 55, 57, 65, 69, 77]
Ns = [55]


for i in range(len(Ns)):
    N = Ns[i]
    n = N.bit_length()
    a = 1
    print(f"\nN: {N}")
    start = time.time()

    tries = 50

    for j in range(tries):
        prime_candidate = getLowLevelPrime(n, N)
        if not isMillerRabinPassed(prime_candidate) or prime_candidate > N or N % prime_candidate == 0:
            continue
        else:
            a = prime_candidate
            break

    if a == 1:
        for j in range(len(first_primes_list)):
            pc = first_primes_list[-(j+1)]
            if pc < N and N % pc != 0:
                a = pc
                break

    print(f"a1: {a}")

    a = 13

    print(f"a2: {a}")

    shor = Shor(shots=128)
    circuit = shor.construct_circuit(a, N, semi_classical=False, measurement=True)
    # circuit.draw(output='mpl', fold=-1)
    result = shor.get_order(a, N, semi_classical=False)

    end = time.time()
    exec_time = (end-start)*(10**3)

    converted_time = convert_milliseconds(exec_time)
    orders = convert_to_order_list(result.all_orders)

    classical_exec_time = result.classical_milliseconds
    classical_converted_time = convert_milliseconds(classical_exec_time)

    result_str = (f"N: {result.N}\n"
                  f"n: {result.n}\n"
                  f"random a: {result.random_prime}\n"
                  f"total_shots: {result.total_shots}\n"
                  f"successful_shots: {result.successful_shots}\n"
                  f"total results count: {result.total_counts}\n"
                  f"successful results count: {result.successful_counts}\n"
                  f"output_data: {result.output_data}\n"
                  f"\nall orders: {orders}\n"
                  f"\norder: {result.order}\n"
                  f"\naverage classical part exec time (ms): {classical_exec_time}\n"
                  f"average classical part exec time: {classical_converted_time}\n"
                  f"\nexec_time (ms): {exec_time} ms\n"
                  f"exec_time: {converted_time}")
    try:
        file = open(f"output_data/shor/N_{N}/a_{a}", "w")
    except FileNotFoundError:
        os.mkdir(f"output_data/shor/N_{N}")
        file = open(f"output_data/shor/N_{N}/a_{a}", "w")

    file.write(result_str)
    file.close()

    print(result_str)
