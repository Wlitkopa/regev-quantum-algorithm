import logging
import math
import time
from abc import ABC, abstractmethod
from fractions import Fraction
from itertools import chain
from typing import Optional, Tuple, Union

import numpy as np
from qiskit import AncillaRegister, ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit.circuit import Instruction
from qiskit.circuit.library import QFT
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator

#from qiskit.utils.validation import validate_min


logger = logging.getLogger(__name__)


class Shor(ABC):

    def __init__(self,  shots) -> None:
        self.shots= shots

    def factor2(self, a: int, N: int, semi_classical: bool):
        shor_result = self.get_order(a, N, semi_classical)
        if shor_result.order:
            order = shor_result.order
            factors = self._get_factors(order, a, N)
            if factors:
                logger.info('Found factors %s from order %s.', factors, order)
                print(f"\nFactors: {factors}\n"
                      f"Order {order}\n")
                return shor_result

        return shor_result

    def factor(self, a: int, N: int, semi_classical: bool) -> Optional[Tuple[int, int]]:
        shor_result = self.get_order(a, N, semi_classical)
        if shor_result.order:
            order = shor_result.order
            factors = self._get_factors(order, a, N)
            if factors:
                logger.info('Found factors %s from order %s.', factors, order)
                return factors

        return None

    def get_order(self, a: int, N: int, semi_classical=False) -> 'ShorResult':
        self._validate_input(a, N)

        result = ShorResult()
        result.N = N
        result.n = N.bit_length()
        result.random_prime = a

        circuit = self.construct_circuit(a, N, semi_classical, measurement=True)
        aersim = AerSimulator()
        pm = generate_preset_pass_manager(backend=aersim, optimization_level=3)
        isa_qc = pm.run(circuit)

        counts = aersim.run(isa_qc,shots=self.shots).result().get_counts(0)
      #  counts = result.get_counts(0)
       # print('Counts(ideal):', counts)

        #counts=self.sampler().run(circuit, shots=self.shots).result().quasi_dists[0].binary_probabilities()

        result.total_counts = len(counts)
        result.total_shots =  self.shots


        all_orders = []

        for measurement, shots in counts.items():
            measurement = self._parse_measurement(measurement, semi_classical)
            start = time.time()
            order = self._get_order(measurement, a, N)
            end = time.time()
            result.classical_milliseconds += (end - start) * 1000


            result.output_data.append([measurement, shots])
            if order:
                if order == 1:
                    logger.info('Skip trivial order.')
                    continue

                if result.order and not result.order == order:
                    logger.error(f'Currently computed order {order} differs from already stored: {result.order}.')
                    all_orders.append([order, shots])
                    continue

                result.order = order
                all_orders.append([order, shots])
                result.successful_counts += 1
                result.successful_shots += shots

        result.classical_milliseconds = result.classical_milliseconds / result.total_counts
        result.all_orders = all_orders
        return result

    def construct_circuit(self, a: int, N: int, semi_classical: bool = False, measurement: bool = True):
        self._validate_input(a, N)

        n = N.bit_length()

        if semi_classical:
            if not measurement:
                raise ValueError('Semi-classical implementation have to contain measurement parts.')
            return self._construct_circuit_with_semiclassical_QFT(a, N, n)
        else:
            return self._construct_circuit(a, N, n, measurement)

    @staticmethod
    def _validate_input(a: int, N: int):
       # validate_min('N', N, 3)
        #validate_min('a', a, 2)

        if N < 1 or N % 2 == 0:
            raise ValueError(f'The input N needs to be an odd integer greater than 1. Provided N = {N}.')
        if a >= N or math.gcd(a, N) != 1:
            raise ValueError(f'The integer a needs to satisfy a < N and gcd(a, N) = 1. Provided a = {a}.')

    @staticmethod
    def _parse_measurement(measurement: str, semi_classical=False):
        if semi_classical:
            measurement = measurement.replace(' ', '')
        return int(measurement, base=2)

    @staticmethod
    def _get_order(measurement: int, a: int, N: int) -> Union[int, None]:
        if measurement == 0:
            logger.info('Measurement = 0, order is trivial: r = 1.')
            return 1

        logger.info(f'Measurement = {measurement}.')
        n = N.bit_length()
        phase = measurement / pow(2, 2 * n)
        logger.info(f'Measured phase = {phase}.')
        fraction = Fraction(phase).limit_denominator(N)
        logger.info(f'Fractional approximation: {fraction}.')

        r = fraction.denominator

        if pow(a, r, mod=N) == 1:
            logger.info(f'Success, order: r = {r} from measurement {measurement}.')
            return r
        else:
            logger.info(f'Denominator {r} is not the order. '
                        f'Trying multiplication for case when numerator and denominator had a common factor.')
            r0 = r
            for i in range(2, n):
                r = i * r0
                if pow(a, r, mod=N) == 1:
                    logger.info(f'Success, order: r = {i}*{r0} = {r}.')
                    return r

            logger.info(f'Multiplication failed, maximum test factor = {n} was too small.')
            return None

    @staticmethod
    def _get_factors(r: int, a: int, N: int) -> Optional[Tuple[int, int]]:
        if r % N == 1:
            logger.info('Odd order, cannot find factors.')
            return None

        guess = math.gcd(pow(a, r // 2) + 1, N)
        if guess in [1, N]:
            logger.info(f'Trivial factor found: {guess}.')
            return 1, N
        else:
            logger.info(f'Non-trivial factor found: {guess}.')
            return guess, N // guess

    def _construct_circuit(self, a: int, N: int, n: int, measurement: bool) -> QuantumCircuit:
        x_qreg = QuantumRegister(2 * n, 'x')
        y_qreg = QuantumRegister(n, 'y')
        aux_qreg = AncillaRegister(self._get_aux_register_size(n), 'aux')

        circuit = QuantumCircuit(x_qreg, y_qreg, aux_qreg, name=self._get_name(a, N))

        circuit.h(x_qreg)
        circuit.x(y_qreg[0])

        modular_exponentiation_gate = self._modular_exponentiation_gate(a, N, n)
        circuit.append(
            modular_exponentiation_gate,
            circuit.qubits
        )

        iqft = QFT(len(x_qreg)).inverse().to_gate()
        circuit.append(
            iqft,
            x_qreg
        )

        if measurement:
            x_creg = ClassicalRegister(2 * n, name='xValue')
            circuit.add_register(x_creg)
            circuit.measure(x_qreg, x_creg)

        return circuit

    def _construct_circuit_with_semiclassical_QFT(self, a: int, N: int, n: int) -> QuantumCircuit:
        x_qreg = QuantumRegister(1, 'x')
        y_qreg = QuantumRegister(n, 'y')
        aux_qreg = AncillaRegister(self._get_aux_register_size(n), 'aux')

        x_creg = [ClassicalRegister(1, f'xV{i}') for i in range(2 * n)]
        aux_creg = ClassicalRegister(1, 'auxValue')

        name = f'{self._get_name(a, N)} (semi-classical QFT)'
        circuit = QuantumCircuit(x_qreg, y_qreg, aux_qreg, *x_creg, aux_creg, name=name)

        circuit.x(y_qreg[0])

        max_i = 2 * n - 1
        for i in range(0, 2 * n):
            circuit.h(x_qreg)

            partial_constant = pow(a, pow(2, max_i - i), mod=N)
            modular_multiplication_gate = self._modular_multiplication_gate(partial_constant, N, n)
            circuit.append(
                modular_multiplication_gate,
                chain([x_qreg[0]], y_qreg, aux_qreg)
            )

            for j in range(i):
                angle = -np.pi / float(pow(2, i - j))
                circuit.p(angle, x_qreg[0]).c_if(x_creg[j], 1)

            circuit.h(x_qreg)
            circuit.measure(x_qreg[0], x_creg[i][0])
            circuit.measure(x_qreg[0], aux_creg[0])
            circuit.x(x_qreg).c_if(aux_creg, 1)

        circuit.measure(x_qreg[0], aux_creg[0])

        return circuit


    @abstractmethod
    def _get_aux_register_size(self, n: int) -> int:
        raise NotImplementedError

    def _get_name(self, a: int, N: int) -> str:
        return f'{self._prefix} Shor(a={a}, N={N})'

    @property
    @abstractmethod
    def _prefix(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def _modular_exponentiation_gate(self, constant: int, N: int, n: int) -> Instruction:
        raise NotImplementedError

    @abstractmethod
    def _modular_multiplication_gate(self, constant: int, N: int, n: int) -> Instruction:
        raise NotImplementedError


class ShorResult():

    def __init__(self) -> None:
        self._order = None
        self._total_counts = 0
        self._successful_counts = 0
        self._total_shots = 0
        self._successful_shots = 0

        self._N = 0
        self._n = 0
        self._random_prime = 0
        self._all_orders = []
        self._output_data = []
        self._classical_milliseconds = 0



    @property
    def order(self) -> Optional[int]:
        return self._order

    @order.setter
    def order(self, value: int) -> None:
        self._order = value

    @property
    def total_counts(self) -> int:
        return self._total_counts

    @total_counts.setter
    def total_counts(self, value: int) -> None:
        self._total_counts = value

    @property
    def successful_counts(self) -> int:
        return self._successful_counts

    @successful_counts.setter
    def successful_counts(self, value: int) -> None:
        self._successful_counts = value

    @property
    def total_shots(self) -> int:
        return self._total_shots

    @total_shots.setter
    def total_shots(self, value: int) -> None:
        self._total_shots = value

    @property
    def successful_shots(self) -> int:
        return self._successful_shots

    @successful_shots.setter
    def successful_shots(self, value: int) -> None:
        self._successful_shots = value


    @property
    def N(self) -> int:
        return self._N

    @N.setter
    def N(self, value: int) -> None:
        self._N = value

    @property
    def n(self) -> int:
        return self._n

    @n.setter
    def n(self, value: int) -> None:
        self._n = value

    @property
    def random_prime(self) -> int:
        return self._random_prime

    @random_prime.setter
    def random_prime(self, value: int) -> None:
        self._random_prime = value

    @property
    def all_orders(self) -> []:
        return self._all_orders

    @all_orders.setter
    def all_orders(self, value: []) -> None:
        self._all_orders = value

    @property
    def output_data(self) -> []:
        return self._output_data

    @output_data.setter
    def output_data(self, value: []) -> None:
        self._output_data = value

    @property
    def classical_milliseconds(self) -> int:
        return self._classical_milliseconds

    @classical_milliseconds.setter
    def classical_milliseconds(self, value: int) -> None:
        self._classical_milliseconds = value


