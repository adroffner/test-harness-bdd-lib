import unittest

from morelia import verify

from pathlib import Path
from calculator.calculator_simulation import Calculator

HOME_DIR = Path(r'C:\Users\adroffner\PycharmProjects')


class CalculatorTests(unittest.TestCase):
    """ Calculator Gherkin Tests.

    Prove Morelia BDD library handles complex Gherkin Syntax such as multiple scenarios.
    """

    FEATURE_DIR = HOME_DIR / r'test-harness-bdd-lib/tests/features/calculator_simulation'

    def setUp(self) -> None:
        self.calculator = Calculator()
        self.calculator.click_power()
        self.sum = None
        self.quotient = None

    def test_addition(self):
        """ Addition feature """
        verify(self.FEATURE_DIR / 'add_calculator.feature', self)

    def test_division(self):
        """ Division feature """
        verify(self.FEATURE_DIR / 'divide_calculator.feature', self)

    # Morelia automated steps
    # =======================

    # Background Steps

    def step_the_Calculator_is_powered_on(self):
        r"""the Calculator is powered on"""
        self.assertTrue(self.calculator.is_power_on)

    # Addition Steps

    def step_I_add_number_and_number(self, number1, number2):
        r"""I add "([^"]+)" and "([^"]+)\""""
        a = float(number1)
        b = float(number2)
        self.sum = a + b
        self.assertEqual(self.sum, self.calculator.add(a, b))

    def step_the_sum_should_be_number(self, number):
        r"""the sum should be "([^"]+)\""""
        expected_sum = float(number)
        self.assertEqual(self.sum, expected_sum)

    # Division Steps

    def step_I_divide_numerator_by_denominator(self, numerator, denominator):
        r"""I divide (.+) by (.+)"""
        a = float(numerator)
        b = float(denominator)
        self.quotient = a / b
        self.assertEqual(self.quotient, self.calculator.divide(a, b))

    def step_the_quotient_should_be_result(self, result):
        r"""the quotient should be (.+)"""
        expected_quotient = float(result)
        self.assertEqual(self.quotient, expected_quotient)


if __name__ == '__main__':
    unittest.main()
