import os
from pathlib import Path


def extract_effectiveness_from_file(filename):
    effectiveness_all_var = None
    effectiveness_nontrivial_var = None
    time_in_ms_var = None

    if os.path.exists(filename):
        with open(filename, 'r') as f:
            content = f.readlines()
            try:
                effectiveness_all_var = float(content[11].split(' ')[-1][:-2])
                effectiveness_nontrivial_var = float(content[12].split(' ')[-1][:-2])
                time_in_ms_var = int(content[15].split(' ')[-2].split('.')[0])
            except IndexError:
                pass
    else:
        print(f"File {filename} does not exist.")

    # print(f"effectiveness_all: {effectiveness_all_var}")
    # print(f"effectiveness_nontrivial: {effectiveness_nontrivial_var}")
    # print(f"time_in_ms: {time_in_ms_var}")

    return effectiveness_all_var, effectiveness_nontrivial_var, time_in_ms_var


if __name__ == "__main__":
    N = "0_1532.3372990219032/N_15"
    file = f"../../../output_data/gauss/classical_part/file_analysis_all_types_with_output_register_measuring_big_R/type_1/floor_floor/{N}"
    extract_effectiveness_from_file(file)
