
from implementations.r_haner import HanerRegev as Regev


# All analysed values
# Ns = [15, 21, 33, 35, 39, 51, 55, 57, 65, 69, 77, 85, 91, 95, 119, 143]
# d_qd_list = [[True, True], [True, False], [False, True], [False, False]]
# type_of_test_array = [1, 2, 3]


# Initiating Regev algorithm class
shots_num = 128
regev = Regev(shots_num)


# Draw quantum circuit
Ns = [21, 33]
d_qd_list = [[True, True], [True, False], [False, True], [False, False]]
decompose = False
# regev.draw_quantum_circuit(Ns, d_qd_list, decompose)


# Run all algorithm
Ns = [21]
d_qd_list = [[False, True], [False, False]]
number_of_combinations = 100
type_of_test = 1
find_pq = True
regev.run_all_algorithm(Ns, d_qd_list, number_of_combinations, type_of_test, find_pq)


# Run quantum part
Ns = [15, 21, 33, 35]
d_qd_list = [[False, False], [True, True]]
# regev.run_quantum_part_data_collection(Ns, d_qd_list)


# Analysing data from a quantum part output file
Ns = [39]
d_qd_list = [[True, True]]
number_of_combinations = 50
type_of_test_array = [1, 2, 3]
# regev.run_file_data_analyzer(Ns, d_qd_list, number_of_combinations, type_of_test_array)


# Run on IBM quantum computer
N = 15
d_ceil_bool = True
qd_ceil_bool = True
# regev.run_on_quantum_computer(N, d_ceil_bool, qd_ceil_bool)

