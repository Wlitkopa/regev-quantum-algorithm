import os
from pathlib import Path
from construct_effectiveness_list import construct_effectiveness_list
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def draw_plot(N_list, d_qd_list, type_of_test_list, meas_R_list):
    effectiveness_all_list = []
    effectiveness_nontrivial_list = []
    time_in_ms_list = []
    filename = ""

    colors = [["red", "orange"], ["blue", "gray"], ["green", "yellowgreen"], ["navy", "purple"]]

    for d_qd in d_qd_list:

        if d_qd[0]:
            d = 'ceil'
        else:
            d = 'floor'

        if d_qd[1]:
            qd = 'ceil'
        else:
            qd = 'floor'

        for j in range(len(type_of_test_list)):
            type_of_test = type_of_test_list[j]
        # for type_of_test in type_of_test_list:

            for i in range(len(meas_R_list)):
            # for meas_R in meas_R_list:

                plt.figure()
                plt.xlabel("N - factorized number")
                plt.ylabel("effectiveness [%]")
                # plt.legend(bbox_to_anchor=(0, 0.92, 1, 0.2), loc="lower left", mode="expand", borderaxespad=0, ncol=3)
                plt.subplots_adjust(bottom=0.48)

                mR_0 = meas_R_list[i][0]
                mR_1 = meas_R_list[i][1]

                if mR_0:
                    output_register_measuring = 'with'
                else:
                    output_register_measuring = 'without'

                if mR_1:
                    R_type = 'big'

                else:
                    R_type = 'small'

                file_dir = f"output_data/gauss/classical_part/file_analysis_all_types_{output_register_measuring}_output_register_measuring_{R_type}_R/type_{type_of_test}/{d}_{qd}"

                # print(f"file_dir: {file_dir}")

                effectiveness_all_list, effectiveness_nontrivial_list, time_in_ms_list = construct_effectiveness_list(N_list, file_dir)

                color_id = i

                # ALL OUTPUT REGS CONFIGURATIONS AND ALL R PARAMETER VALUES ONE TEST TYPE
                plt.plot(N_list[:len(effectiveness_all_list)], effectiveness_all_list,
                             label=f"Square root of unity modulo N, {output_register_measuring} output registry measuring, {R_type} R",
                             color=colors[color_id - 1][0], marker='o')
                plt.plot(N_list[:len(effectiveness_nontrivial_list)], effectiveness_nontrivial_list,
                         label=f"Non-trivial square root of unity modulo N, {output_register_measuring} output registry measuring, {R_type} R",
                         color=colors[color_id - 1][1], marker='o')


                # ALL OUTPUT REGS CONFIGURATIONS AND ALL R PARAMETER VALUES ONE TEST TYPE
                plt.title(f"Regev's algorithm effectiveness for {d}_{qd} and test type {type_of_test}")

                # PLOT CONFIG
                plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=1, frameon=False)
                plt.grid(color='gray', linestyle='--', linewidth=0.25)

                # MANIPULATING X-axis
                # ax = plt.gca()
                # ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
                # ax.xaxis.set_major_locator(ticker.MultipleLocator(5))

                # ALL OUTPUT REGS CONFIGURATIONS AND ALL R PARAMETER VALUES ONE TEST TYPE
                # plt.savefig(f"../../../images/plots/effectiveness_gauss/effectiveness_{d}_{qd}_test_type_{type_of_test}_{output_register_measuring}_{R_type}.png")
                # print(f"CREATED PLOT: images/plots/effectiveness_gauss/effectiveness_{d}_{qd}_test_type_{type_of_test}_{output_register_measuring}_{R_type}.png")

                plt.savefig(f"../../../images/plots/effectiveness_gauss/effectiveness_{d}_{qd}_test_type_{type_of_test}_{output_register_measuring}_{R_type}.svg", format="svg")
                print(f"CREATED PLOT: images/plots/effectiveness_gauss/effectiveness_{d}_{qd}_test_type_{type_of_test}_{output_register_measuring}_{R_type}.svg")

                plt.close()


if __name__ == "__main__":
    # N_list = [15, 21, 33, 35, 39]
    # d_qd_list = [[True, True], [True, False], [False, True], [False, False]]
    # type_of_test_list = [1, 2, 3]
    # meas_R_list = [[True, True], [True, False], [False, True], [False, False]]

    N_list = [15, 21, 33, 35, 39]
    d_qd_list = [[False, False]]
    type_of_test_list = [1, 2, 3]
    # type_of_test_list = [3]
    meas_R_list = [[True, True], [True, False], [False, True], [False, False]]
    # meas_R_list = [[True, True], [True, False], [False, True]]

    color_id = 0

    draw_plot(N_list, d_qd_list, type_of_test_list, meas_R_list)

