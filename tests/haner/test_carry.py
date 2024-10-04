import unittest

from tests.haner.gate_tests.carry import Test


class CarryTestCase(unittest.TestCase):
    def test_passing_wrong_value_for_constant(self):
        n = 4
        x = 8
        g = 3

        constant = -1
        with self.assertRaises(ValueError):
            test = Test(constant, n, self)
            test.run({'x': x, 'g': g})

        constant = 16
        with self.assertRaises(OverflowError):
            test = Test(constant, n, self)
            test.run({'x': x, 'g': g})

    def test_for_1_qubit(self):
        self._test_for_n_qubits(1, [0, 1], None)

    def test_flipping_c_for_1_qubit(self):
        self._test_flipping_c_for_n_qubits(1, 1, 1, None)

    def test_for_2_qubits(self):
        self._test_for_n_qubits(2, [0, 1, 2, 3], 1)

    def test_dirty_register_for_2_qubits(self):
        self._test_dirty_register_for_n_qubits(2, 2, 1, [0, 1])

    def test_flipping_c_for_2_qubits(self):
        self._test_flipping_c_for_n_qubits(2, 2, 1, 1)

    def test_for_3_qubits(self):
        self._test_for_n_qubits(3, [0, 1, 3, 5, 6, 7], 2)

    def test_dirty_register_for_3_qubits(self):
        self._test_dirty_register_for_n_qubits(3, 5, 4, [0, 1, 2, 3])

    def test_flipping_c_for_3_qubits(self):
        self._test_flipping_c_for_n_qubits(3, 5, 4, 2)

    def test_for_4_qubits(self):
        self._test_for_n_qubits(4, [0, 1, 5, 10, 12, 14, 15], 5)

    def test_dirty_register_for_4_qubits(self):
        self._test_dirty_register_for_n_qubits(4, 12, 7, [0, 1, 5, 6, 7])

    def test_flipping_c_for_4_qubits(self):
        self._test_flipping_c_for_n_qubits(4, 12, 7, 5)

    def test_for_5_qubits(self):
        self._test_for_n_qubits(5, [0, 1, 8, 17, 25, 30, 31], 10)

    def test_dirty_register_for_5_qubits(self):
        self._test_dirty_register_for_n_qubits(5, 25, 8, [0, 1, 5, 10, 14, 15])

    def test_flipping_c_for_5_qubits(self):
        self._test_flipping_c_for_n_qubits(5, 25, 8, 10)

    def _test_for_n_qubits(self, n, values, g):
        for constant in values:
            with self.subTest(constant=constant):
                params = [{'x': x, 'g': g, 'c': 0} for x in values]

                test = Test(constant, n, self)
                test.run_subtests(params)

    def _test_dirty_register_for_n_qubits(self, n, constant, x, g_values):
        params = [{'x': x, 'g': g, 'c': 0} for g in g_values]
        test = Test(constant, n, self)
        test.run_subtests(params)

    def _test_flipping_c_for_n_qubits(self, n, constant, x, g):
        c_values = [0, 1]
        params = [{'x': x, 'g': g, 'c': c} for c in c_values]
        test = Test(constant, n, self)
        test.run_subtests(params)
