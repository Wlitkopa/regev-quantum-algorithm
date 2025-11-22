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


# Initiating Regev algorithm class
shots_num = 128
regev = Regev(shots_num)

# Numbers N (for running 'all parts', 'quantum part', 'classical part' and 'drawing quantum circuit')
Ns = [15, 21]
# Ns = [15]
# Ns = [15, 21, 33, 35, 39, 51, 55, 57, 65, 69, 77, 85, 91, 95, 119, 143]
# Ns = [85, 91, 95, 119, 143]


# d and qd parameters combination (for running 'all parts', 'quantum part', 'classical part' and 'drawing quantum circuit')
# d_qd_list = [[False, True], [False, False]]
# d_qd_list = [[True, True], [False, False]]
d_qd_list = [[False, False]]
# d_qd_list = [[True, False]]

# Number of combinations of picking up output vectors to create lattice (for running 'all parts', 'classical part')
number_of_combinations = 100

# Type of method of picking up output vectors to create lattice (for running 'all parts')
type_of_test = 1

# Type of method of picking up output vectors to create lattice (for running 'classical part')
type_of_test_array = [1, 2, 3]

# Parameter indicating if a trivial final part of finding p and q should be run (for running 'all parts')
find_pq = True

# Parameter denoting if a decomposed version of quantum circuit should be drawn (drawing quantum circuit)
decompose = False

# Parameter initiating initial superposition in gaussian distribution [mu, sigma]
# gauss_init = False
gauss_init = [0, False]
# gauss_init = [False, 2**(Ns[0].bit_length() - 3)]
# gauss_init = [False, False]
# gauss_init = [0, 11]

# Output registry measuring
measure_output_register = True



while True:
    print("========== REGEV'S ALGORITHM ==========\n")

    print('''Choose an option:
    1. Run all algorithm
    2. Run quantum part
    3. Run classical part
    4. Draw quantum circuit
    5. Exit''')

    while True:
        try:
            choice = int(input())
            break
        except ValueError:
            print("Please enter a number.")
            continue

    match choice:
        case 1:
            print("------- Running all algorithm -------")
            regev.run_all_algorithm(Ns, d_qd_list, number_of_combinations, type_of_test, find_pq, gauss_init, measure_output_register)
            print("Finished running all algorithm. The results are saved in output_data/regev/all_parts folder")
            continue

        case 2:
            print("------- Running quantum part -------")
            regev.run_quantum_part_data_collection(Ns, d_qd_list, gauss_init, measure_output_register)
            print("Finished running quantum part. The results are saved in output_data/regev/quantum_part folder")
            continue

        case 3:
            print("------- Running classical part -------")
            regev.run_file_data_analyzer(Ns, d_qd_list, number_of_combinations, type_of_test_array)
            print("Finished running classical part. The results are saved in output_data/regev/classical_part folder")
            continue

        case 4:
            print("------- Drawing quantum circuit -------")
            regev.draw_quantum_circuit(Ns, d_qd_list, decompose, gauss_init, measure_output_register)
            print("Finished running drawing quantum circuit")
            continue

        case 5:
            print("Exiting...")
            exit(0)

        case _:
            print("Invalid choice.")

