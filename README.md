# Regev's Algorithm for IBM Qiskit

This repository contains an implementation of the quantum Regev's algorithm. Its input
registers are initialised in a multidimensional Gaussian superposition prepared with
the Grover–Rudolph state-preparation gate. The algorithm is executed on a local
quantum computer simulator using IBM Qiskit, optionally accelerated with CUDA /
cuQuantum for larger circuits.

## Requirements

* Python version >= 3.11
* An NVIDIA GPU with a working CUDA install (only if you want the GPU /
  cuQuantum backend; remove the `device="GPU"` / `cuStateVec_enable=True`
  kwargs in `implementations/regev_parts/simulation.py` to run on CPU).

## Installation

1. Clone the repository and navigate to the project directory.
```bash
git clone https://github.com/Wlitkopa/regev-quantum-algorithm.git

cd regev-quantum-algorithm
```

2. Create and activate a virtual environment.
```bash
python3.11 -m venv .venv
echo 'unset LD_LIBRARY_PATH' >> .venv/bin/activate
source .venv/bin/activate
```

3. Install the required dependencies.

```bash
pip install -r requirements.txt
```

## Usage

To run the Regev's algorithm interactively, execute the following script:

```bash
python regev_all.py
```

Edit the configuration block at the top of the script (`Ns`, `d_qd_list`,
`gauss_init`, `meas_R_list`, …) before running; each option is documented
inline. A non-interactive driver that runs the quantum part, classical
replay, and circuit drawing back-to-back is provided for cluster
submissions:

```bash
python regev_all_noninteractive.py
```

## Images and data

The generated artefacts are written locally and are not tracked by git.

### Quantum Circuits

The quantum circuit images for different parameter configurations are stored under:

- **images/&lt;main_path_dir&gt;/quantum_part/…/N_&lt;N&gt;.svg:** General form of the circuit.
- **images/&lt;main_path_dir&gt;/quantum_part/…/N_&lt;N&gt;_decomposed.svg:** Version with the top-level gates decomposed.

The Gaussian initial-state probability plots (`line_points.svg`, `diagram.svg`,
`line_points_cont.svg`) are written alongside the circuit image.

### Output Data

The data obtained from running Regev's algorithm (and Shor's, via
`shor_all.py`) is stored under:

- **output_data**

### Plots

Graphs representing the research data depending on various parameters are
produced by the scripts under `utils/plots/` and stored under:

- **images/plots**


## Acknowledgement

This project uses code provided by **Bartłomiej Stępień**, licensed under the Apache License 2.0 available
at <https://github.com/bartek-bartlomiej/master-thesis>.

Copyright (c) 2023 Bartłomiej Stępień

The original implementation of this repository (2024) was co-authored by **Natalia Moćko** and **Przemysław Pawlitko**,
released under the Apache License 2.0.

## License

Copyright (c) 2024 Natalia Moćko, Przemysław Pawlitko (original implementation)
Copyright (c) 2025-2026 Przemysław Pawlitko (Grover–Rudolph extension and subsequent modifications)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at <http://www.apache.org/licenses/LICENSE-2.0>.

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
