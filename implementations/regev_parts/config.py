"""Small typed helpers that translate the ``meas_R_list`` and ``d_qd`` flags.

The legacy call sites pass raw nested lists (e.g. ``[[True, False], ...]``).
Converting them into a named structure once, at the top of each entry point,
lets the rest of the code refer to ``cfg.measure_output_register`` rather than
``meas_R_list[s][0]``.
"""

from dataclasses import dataclass
from typing import List, Optional, Sequence

# Sentinel meas_R_list value meaning "qubits were initialised with a uniform
# (Hadamard) superposition; no Gaussian init, no R variant to choose".
UNIFORM_INIT_SENTINEL: List[int] = [0]


@dataclass(frozen=True)
class MeasRConfig:
    """One entry of ``meas_R_list`` in a readable form."""

    measure_output_register: bool
    is_R_big: bool

    @property
    def measuring_output_register(self) -> str:
        return "with" if self.measure_output_register else "without"

    @property
    def param_R(self) -> str:
        return "big" if self.is_R_big else "small"


def is_uniform_init(meas_R_list: Sequence) -> bool:
    """True if the caller wants uniform (Hadamard) init, not Gaussian."""
    return len(meas_R_list) > 0 and meas_R_list[0] == 0


def parse_meas_R_entry(entry) -> Optional[MeasRConfig]:
    """Convert one ``meas_R_list`` entry to a :class:`MeasRConfig` (or ``None``).

    Returns ``None`` when the entry is the uniform-init sentinel; callers can
    then branch cheaply on that.
    """
    if entry == 0:
        return None
    return MeasRConfig(measure_output_register=bool(entry[0]), is_R_big=bool(entry[1]))


def mode_name(is_ceil: bool) -> str:
    """``True`` → ``"ceil"``, ``False`` → ``"floor"`` — used in path names."""
    return "ceil" if is_ceil else "floor"
