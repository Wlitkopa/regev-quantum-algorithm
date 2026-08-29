#!/usr/bin/env python3
"""Non-interactive entry point — runs quantum part, classical part and circuit
drawing back-to-back with the configuration in the header. Useful for cluster
submissions where stdin is not available. See :mod:`regev_all` for a documented
description of each parameter.
"""

from implementations.r_haner import HanerRegev as Regev

shots_num = 128
main_path_dir = "regev_run_noninteractive"
regev = Regev(shots_num, main_path_dir)

Ns = [15, 21]
d_qd_list = [[True, True]]
number_of_combinations = 100
type_of_test = 1
type_of_test_array = [1, 2, 3]
find_pq = True
decompose = True

# gauss_init options:
#   False               — disable Gaussian init; the input registers are initialised
#                         with a uniform (Hadamard) superposition instead.
#   [False, False]      — enable with data-driven default mu and sigma.
#   [0, False]          — mu = 0, sigma from the default.
#   [0, 11]             — explicit mu and sigma.
gauss_init = [0, False]

# meas_R_list options:
#   [0]                              — uniform (Hadamard) init; use this whenever
#                                      gauss_init = False.
#   [[True,  True], [True,  False]]  — with output-register measure, both R variants.
#   [[False, True], [False, False]]  — without output-register measure, both R variants.
meas_R_list = [[True, True], [True, False]]

# Only used when meas_R_list = [0] (uniform init). For Gaussian init each
# meas_R_list entry carries its own measure-output-register flag, so this
# variable is ignored.
measure_output_register = True

# use_grover_rudolph options:
#   True   — build the Gaussian input state with the Grover-Rudolph gate
#            (works on real quantum hardware and on the simulator).
#   False  — inject the amplitudes directly via ``circuit.initialize``
#            (simulator only; not a real-hardware gate sequence).
use_grover_rudolph = True


def main() -> None:
    print("------- Running quantum part -------")
    regev.run_quantum_part_data_collection(
        Ns, d_qd_list, gauss_init, measure_output_register,
        meas_R_list, use_grover_rudolph,
    )
    print("Finished running quantum part")

    print("------- Running classical part -------")
    regev.run_file_data_analyzer(
        Ns, d_qd_list, number_of_combinations,
        type_of_test_array, meas_R_list,
    )
    print("Finished running classical part")

    print("------- Drawing quantum circuit -------")
    regev.draw_quantum_circuit(
        Ns, d_qd_list, decompose, gauss_init,
        meas_R_list, use_grover_rudolph,
        measure_output_register,
    )
    print("Finished drawing quantum circuit")


if __name__ == "__main__":
    main()
