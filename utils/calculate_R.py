
import math
import itertools

def calculate_R(d, qd, N, n, a):

    a_root = []

    for a_ in a:
        a_root.append(int(math.sqrt(a_)))
    m = math.ceil(n / d) + 2
    powers = []
    for i in range(m):
        powers.append(i)

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

    R = math.ceil(6 * T * math.sqrt((d + 5) * (2 * d + 4) * (d / 2)) * (2 ** ((n + 1) / (d + 4) + d + 2)))

    return R

