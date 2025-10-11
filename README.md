# Regev's Algorithm for IBM Qiskit

This repository contains an implementation of the quantum Regev's algorithm. It is executed on a local quantum computer simulator using IBM Qiskit.

## Requirements

* Python version >= 3.11

## Installation

1. Clone the repository and navigate to the project directory.
```bash
git clone https://github.com/Wlitkopa/regev-quantum-algorithm.git

cd regev-quantum-algorithm
```

2. Create and activate a virtual environment.
```bash
python -m venv venv

source venv/bin/activate
```

3. Install the required dependencies.

```bash
pip install -r requirements.txt
```

## Usage

To run the Regev's algorithm, execute the following script:

```bash
python regev_all.py
```


## Images and data

### Quantum Circuits

The quantum circuits images for different parameter configurations are available in the following folders:

- **images/general:** Contains the most general forms of the quantum circuits.
- **images/decomposed:** Contains slightly more detailed versions of the circuits, where one quantum gate type is decomposed into smaller gates.

### Output Data

The data obtained from running Shor's and Regev's algorithms is stored in the folder:

- **output_data**

### Plots

Graphs representing the research data depending on various parameters are stored in the folder:

- **images/plots**

## Acknowledgement

This project uses code provided by **Bartłomiej Stępień**, licensed under the Apache License 2.0 avilable
at https://github.com/bartek-bartlomiej/master-thesis.

Copyright (c) 2023 Bartłomiej Stępień

## License

Copyright (c) 2024 Natalia Moćko, Przemysław Pawlitko

Licensed under the Apache License, Version 2.0 (the "License"); 
you may not use this file except in compliance with the License. 
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0.

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on 
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the 
specific language governing permissions and limitations under the License.
