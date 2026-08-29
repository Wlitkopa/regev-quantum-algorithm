#!/usr/bin/env python3
"""Interactive entry point for Regev's algorithm with a Gaussian initial state.

Edit the configuration block below, then run with ``python regev_all.py`` and
pick one of the numbered actions from the prompt. For a non-interactive one-shot
run, see :mod:`regev_all_noninteractive`.

Configuration keys explained inline:

* ``Ns``                   — factorisation targets (odd composites).
* ``d_qd_list``            — each entry is ``[d_ceil, qd_ceil]`` (bool pair),
                             which switches ``ceil`` vs ``floor`` for ``d`` and
                             ``qd`` register sizing.
* ``number_of_combinations`` — how many random ``d+4``-vector samples to draw
                             for the LLL step.
* ``type_of_test``         — 1: use real quantum-produced vectors with weights,
                             2: distinct vectors only, 3: uniformly random.
* ``gauss_init``           — ``False`` disables the Gaussian init (falls back to
                             Hadamard uniform init). Otherwise a two-item list
                             ``[mu, sigma]``; either entry may be ``False`` to
                             pick a data-driven default.
* ``meas_R_list``          — list of ``[measure_output_register, is_R_big]``
                             flag pairs. Special sentinel ``[0]`` marks the
                             uniform-init (no-Gaussian) file layout.
* ``use_grover_rudolph``   — ``True`` builds the Gaussian state with the
                             Grover-Rudolph gate (works on real hardware);
                             ``False`` uses ``circuit.initialize`` (simulator only).
"""

from implementations.r_haner import HanerRegev as Regev

# --- Regev instance -------------------------------------------------------

shots_num = 128
main_path_dir = "regev_run_4"
regev = Regev(shots_num, main_path_dir)


# --- Run configuration ----------------------------------------------------

Ns = [15]
d_qd_list = [[False, True]]
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
meas_R_list = [[False, True], [True, False]]

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


def _prompt_choice() -> int:
    while True:
        try:
            return int(input())
        except ValueError:
            print("Please enter a number.")


def main() -> None:
    while True:
        print("========== REGEV'S ALGORITHM ==========\n")
        print(
            """Choose an option:
    1. Run all algorithm
    2. Run quantum part
    3. Run classical part
    4. Draw quantum circuit
    5. Exit"""
        )

        choice = _prompt_choice()

        match choice:
            case 1:
                print("------- Running all algorithm -------")
                regev.run_all_algorithm(
                    Ns, d_qd_list, number_of_combinations, type_of_test,
                    find_pq, gauss_init, meas_R_list, use_grover_rudolph,
                    measure_output_register,
                )
                print("Finished running all algorithm")
            case 2:
                print("------- Running quantum part -------")
                regev.run_quantum_part_data_collection(
                    Ns, d_qd_list, gauss_init, measure_output_register,
                    meas_R_list, use_grover_rudolph,
                )
                print("Finished running quantum part")
            case 3:
                print("------- Running classical part -------")
                regev.run_file_data_analyzer(
                    Ns, d_qd_list, number_of_combinations,
                    type_of_test_array, meas_R_list,
                )
                print("Finished running classical part")
            case 4:
                print("------- Drawing quantum circuit -------")
                regev.draw_quantum_circuit(
                    Ns, d_qd_list, decompose, gauss_init,
                    meas_R_list, use_grover_rudolph,
                    measure_output_register,
                )
                print("Finished drawing quantum circuit")
            case 5:
                print("Exiting...")
                return
            case _:
                print("Invalid choice.")


if __name__ == "__main__":
    main()
