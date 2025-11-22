
from typing import Union, Tuple, Optional


class RegevResult:

    def __init__(self) -> None:
        self._order = None
        self._total_counts = 0
        self._successful_counts = 0
        self._total_shots = 0
        self._successful_shots = 0

        self._N = 0
        self._n = 0
        self._d_ceil = False
        self._qd_ceil = False
        self._number_of_primes = 0
        self._exp_register_width = 0
        self._squared_primes = []
        self._output_data = []
        self._vectors = []
        self._quantum_exec_time = 0

        self._R = 0
        self._T = 0
        self._t = 0
        self._delta = 0
        self._delta_inv = 0
        self._vector = 0
        self._p = 0
        self._q = 0
        self._classical_exec_time = 0

        self._gauss_init_mu = 0
        self._gauss_init_sigma = 0
        self._gauss_R = 0
        self._gauss_mu = 0
        self._gauss_sigma = 0
        self._amps = []

        self._state = []
        self._probs = []
        self._probs_sum = 0

        self._measure_output_register = False


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
    def d_ceil(self) -> bool:
        return self._d_ceil

    @d_ceil.setter
    def d_ceil(self, value: bool) -> None:
        self._d_ceil = value

    @property
    def qd_ceil(self) -> bool:
        return self._qd_ceil

    @qd_ceil.setter
    def qd_ceil(self, value: bool) -> None:
        self._qd_ceil = value

    @property
    def number_of_primes(self) -> int:
        return self._number_of_primes

    @number_of_primes.setter
    def number_of_primes(self, value: int) -> None:
        self._number_of_primes = value

    @property
    def exp_register_width(self) -> int:
        return self._exp_register_width

    @exp_register_width.setter
    def exp_register_width(self, value: int) -> None:
        self._exp_register_width = value

    @property
    def squared_primes(self) -> []:
        return self._squared_primes

    @squared_primes.setter
    def squared_primes(self, value: []) -> None:
        self._squared_primes = value

    @property
    def output_data(self) -> []:
        return self._output_data

    @output_data.setter
    def output_data(self, value: []) -> None:
        self._output_data = value

    @property
    def vectors(self) -> []:
        return self._vectors

    @vectors.setter
    def vectors(self, value: []) -> None:
        self._vectors = value

    @property
    def quantum_exec_time(self) -> int:
        return self._quantum_exec_time

    @quantum_exec_time.setter
    def quantum_exec_time(self, value: int) -> None:
        self._quantum_exec_time = value



    @property
    def R(self) -> int:
        return self._R

    @R.setter
    def R(self, value: int) -> None:
        self._R = value

    @property
    def T(self) -> int:
        return self._T

    @T.setter
    def T(self, value: int) -> None:
        self._T = value

    @property
    def t(self) -> int:
        return self._t

    @t.setter
    def t(self, value: int) -> None:
        self._t = value

    @property
    def delta(self) -> int:
        return self._delta

    @delta.setter
    def delta(self, value: int) -> None:
        self._delta = value

    @property
    def delta_inv(self) -> int:
        return self._delta_inv

    @delta_inv.setter
    def delta_inv(self, value: int) -> None:
        self._delta_inv = value

    @property
    def vector(self) -> []:
        return self._vector

    @vector.setter
    def vector(self, value: []) -> None:
        self._vector = value

    @property
    def p(self) -> int:
        return self._p

    @p.setter
    def p(self, value: int) -> None:
        self._p = value

    @property
    def q(self) -> int:
        return self._q

    @q.setter
    def q(self, value: int) -> None:
        self._q = value

    @property
    def classical_exec_time(self) -> int:
        return self._classical_exec_time

    @classical_exec_time.setter
    def classical_exec_time(self, value: int) -> None:
        self._classical_exec_time = value


    @property
    def gauss_init_mu(self):
        return self._gauss_init_mu

    @gauss_init_mu.setter
    def gauss_init_mu(self, value) -> None:
        self._gauss_init_mu = value

    @property
    def gauss_init_sigma(self):
        return self._gauss_init_sigma

    @gauss_init_sigma.setter
    def gauss_init_sigma(self, value) -> None:
        self._gauss_init_sigma = value

    @property
    def gauss_R(self) -> int:
        return self._gauss_R

    @gauss_R.setter
    def gauss_R(self, value: int) -> None:
        self._gauss_R = value

    @property
    def gauss_mu(self) -> int:
        return self._gauss_mu

    @gauss_mu.setter
    def gauss_mu(self, value: int) -> None:
        self._gauss_mu = value

    @property
    def gauss_sigma(self) -> int:
        return self._gauss_sigma

    @gauss_sigma.setter
    def gauss_sigma(self, value: int) -> None:
        self._gauss_sigma = value

    @property
    def amps(self) -> []:
        return self._amps

    @amps.setter
    def amps(self, value: []) -> None:
        self._amps = value



    @property
    def state(self) -> []:
        return self._state

    @state.setter
    def state(self, value: []) -> None:
        self._state = value

    @property
    def probs(self) -> []:
        return self._probs

    @probs.setter
    def probs(self, value: []) -> None:
        self._probs = value

    @property
    def probs_sum(self) -> int:
        return self._probs_sum

    @probs_sum.setter
    def probs_sum(self, value: int) -> None:
        self._probs_sum = value


    @property
    def measure_output_register(self) -> bool:
        return self._measure_output_register

    @measure_output_register.setter
    def measure_output_register(self, value: bool) -> None:
        self._measure_output_register = value