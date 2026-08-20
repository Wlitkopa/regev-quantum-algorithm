from qiskit.circuit import Instruction

from gates.haner.modular_exponentiation import (
    controlled_modular_multiplication_gate,
    modular_exponentiation_gate,
)
from implementations.shor import Shor


class HanerShor(Shor):
    """Shor driver using the Häner-style modular arithmetic gate set."""

    def _get_aux_register_size(self, n: int) -> int:
        return n + 1

    @property
    def _prefix(self) -> str:
        return "Haner"

    def _modular_exponentiation_gate(self, constant: int, N: int, n: int) -> Instruction:
        return modular_exponentiation_gate(constant, N, n)

    def _modular_multiplication_gate(self, constant: int, N: int, n: int) -> Instruction:
        return controlled_modular_multiplication_gate(constant, N, n)
