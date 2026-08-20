"""AerSimulator configuration and post-simulation data collection."""

from qiskit import transpile
from qiskit_aer import AerSimulator

from utils.convert_measurement import convert_measurement
from utils.regev_result import RegevResult


def build_simulator(shots: int) -> AerSimulator:
    """GPU + cuQuantum simulator matching the Athena-cluster configuration.

    Falls back gracefully to CPU when the GPU backend is unavailable; the Aer
    device selection is otherwise identical to what was used to produce the
    experimental data reported in the thesis.
    """
    return AerSimulator(
        device="GPU",
        cuStateVec_enable=True,
        max_parallel_threads=32,
        max_parallel_experiments=4,
        method="statevector",
        shots=shots,
        blocking_enable=True,
        blocking_qubits=30,
    )


def collect_counts(counts, measure_output_register: bool, result: RegevResult, shots: int) -> None:
    """Fold the ``get_counts`` dictionary into ``result.output_data``.

    When the output register is measured we group by the input-register vector
    (aggregating shot counts for identical input vectors), so downstream code
    receives one row per distinct vector even if ``y`` measurements differ.
    """
    result.total_counts = len(counts)
    result.total_shots = shots
    sorted_counts_items = sorted(counts.items(), key=lambda x: x[1])

    if measure_output_register:
        for measurement, shots_i in sorted_counts_items:
            vector = convert_measurement(measurement)
            for item in result.output_data:
                if item[0] == vector[:-1]:
                    item[2] += shots_i
                    break
            else:
                input_registers = " ".join(measurement.split()[:-1])
                result.output_data.append([vector[:-1], input_registers, shots_i])

            result.output_data_original.append([vector, measurement, shots_i])
            result.successful_counts += 1
            result.successful_shots += shots_i
    else:
        for measurement, shots_i in sorted_counts_items:
            vector = convert_measurement(measurement)
            result.output_data.append([vector, measurement, shots_i])
            result.vectors.append(vector)
            result.successful_counts += 1
            result.successful_shots += shots_i


def run_circuit(circuit, aersim: AerSimulator, shots: int):
    """Transpile and execute a circuit; return the raw counts dictionary."""
    transpiled = transpile(circuit, aersim)
    return aersim.run(transpiled, shots=shots).result().get_counts(0)
