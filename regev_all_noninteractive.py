from sympy.core.random import choice

from implementations.r_haner import HanerRegev as Regev

# Set the following parameters according to the needs

# Possible parameters values for Ns, d_qd_list and type_of_test_array variables
# Ns = [15, 21, 33, 35, 39, 51, 55, 57, 65, 69, 77, 85, 91, 95, 119, 143]
# d_qd_list = [[True, True], [True, False], [False, True], [False, False]]
# type_of_test_array = [1, 2, 3]
# gauss_init = [False, False]  # Sets default values for mu and sigma
# gauss_init = False           # Disables gaussian superposition
# gauss_init = [0, False]      # Sets mu = 0 and sigma is default
# meas_R_list = [0] # Analyse Regev quantum results weren't initialized with Gaussian superposition
# meas_R_list = [[True, True], [True, False], [False, True], [False, False]]


# Initiating Regev algorithm class
shots_num = 128
main_path_dir = "ultimate_test"
regev = Regev(shots_num, main_path_dir)

# Numbers N (for running 'all parts', 'quantum part', 'classical part' and 'drawing quantum circuit')
# Ns = [21]
Ns = [15, 21]
# Ns = [39]
# Ns = [57]
# Ns = [55]
# Ns = [85, 91, 95, 119, 143]
# Ns = [15, 21, 33, 35, 39]
# Ns = [15, 21, 33, 35, 39, 51, 55, 57, 65, 69, 77, 85, 91, 95, 119]
# Ns = [57, 65, 69, 77, 85, 91, 95, 119]
# Ns = [143]

# d and qd parameters combination (for running 'all parts', 'quantum part', 'classical part' and 'drawing quantum circuit')
# d_qd_list = [[False, False]]
# d_qd_list = [[True, True], [False, False]]
# d_qd_list = [[False, False]]
d_qd_list = [[True, True]]
# d_qd_list = [[True, True], [True, False], [False, True], [False, False]]

# d_qd_list = [[True, False]]
# d_qd_list = [[False, False]]

# Number of combinations of picking up output vectors to create lattice (for running 'all parts', 'classical part')
number_of_combinations = 100

# Type of method of picking up output vectors to create lattice (for running 'all parts')
type_of_test = 1

# Type of method of picking up output vectors to create lattice (for running 'classical part')
type_of_test_array = [1, 2, 3]

# Parameter indicating if a trivial final part of finding p and q should be run (for running 'all parts')
find_pq = True

# Parameter denoting if a decomposed version of quantum circuit should be drawn (drawing quantum circuit)
decompose = True

# Parameter initiating initial superposition in gaussian distribution [mu, sigma]
# gauss_init = False
gauss_init = [0, False]
# gauss_init = [False, 2**(Ns[0].bit_length() - 3)]
# gauss_init = [False, False]
# gauss_init = [0, 11]

# Output registry measuring
measure_output_register = True

# List of config for file_data_analyzer method to analyze proper file
# First "True" denotes whether the output register should be measured
# Second "True" denotes whether R parameter should be in "big" mode
# If meas_R_list is [0], then method assumes that the data wasn't initialized with Gaussian superposition
# meas_R_list = [[False, False]]
meas_R_list = [[True, True], [True, False]]
# meas_R_list = [[True, True]]
# meas_R_list = [[True, False]]
# meas_R_list = [0]

# Using grover-rudolph gate for initial Gaussian superposition
use_grover_rudolph = True


print("------- Running quantum part -------")
regev.run_quantum_part_data_collection(Ns, d_qd_list, gauss_init, measure_output_register, meas_R_list,
                                       use_grover_rudolph)
print("Finished running quantum part")

print("------- Running classical part -------")
regev.run_file_data_analyzer(Ns, d_qd_list, number_of_combinations, type_of_test_array, meas_R_list)
print("Finished running classical part")

print("------- Drawing quantum circuit -------")
regev.draw_quantum_circuit(Ns, d_qd_list, decompose, gauss_init, meas_R_list, use_grover_rudolph)
print("Finished running drawing quantum circuit")

