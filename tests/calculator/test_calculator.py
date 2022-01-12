import unittest

from morelia import verify

from pathlib import Path
from calculator.calculator_simulation import Calculator

HOME_DIR = Path(r'C:\Users\adroffner\PycharmProjects')


class AddCalculatorTests(unittest.TestCase):
    """ Add Calculator Gherkin Tests.

    Prove Morelia BDD library handles complex Gherkin Syntax such as multiple scenarios.
    """

    FEATURE_DIR = HOME_DIR / r'test-harness-bdd-lib/tests/features/calculator_simulation'

    def setUp(self) -> None:
        self.calculator = Calculator()
        self.calculator.click_power()
        self.sum = None

    def test_addition(self):
        """ Addition feature """
        verify(self.FEATURE_DIR / 'add_calculator.feature', self)

    # Morelia automated steps

    def step_the_Calculator_is_powered_on(self):
        r"""the Calculator is powered on"""
        self.assertTrue(self.calculator.is_power_on)

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


if __name__ == '__main__':
    unittest.main()
