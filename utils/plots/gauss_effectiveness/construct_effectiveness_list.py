import os
from pathlib import Path
from extract_effectiveness import extract_effectiveness_from_file



def construct_effectiveness_list(N_list, file_dir):
    effectiveness_all_list = []
    effectiveness_nontrivial_list = []
    time_in_ms_list = []
    filename = ""

    for N in N_list:

        # print(f"file_dir: {file_dir}")

        root_dir = Path(f"../../../{file_dir}")
        target = f"N_{N}"

        for p in root_dir.rglob(target):
            # print("Found:", p)
            filename = str(p)

        # print(f"filename: {filename}")

        eff_all, eff_nontrivial, time_in_ms = extract_effectiveness_from_file(filename)

        effectiveness_all_list.append(eff_all)
        effectiveness_nontrivial_list.append(eff_nontrivial)
        time_in_ms_list.append(time_in_ms)

    # print(f"effectiveness_all_list: {effectiveness_all_list}")
    # print(f"effectiveness_nontrivial_list: {effectiveness_nontrivial_list}")
    # print(f"time_in_ms_list: {time_in_ms_list}")

    return effectiveness_all_list, effectiveness_nontrivial_list, time_in_ms_list


if __name__ == "__main__":
    N_list = [15, 21, 33, 35, 39]
    file_dir = "output_data/gauss/classical_part/file_analysis_all_types_with_output_register_measuring_big_R/type_1/floor_floor"

    construct_effectiveness_list(N_list, file_dir)

