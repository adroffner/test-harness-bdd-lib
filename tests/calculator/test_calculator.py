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

    def test_buttons(self):
        """ Addition feature """
        verify(self.FEATURE_DIR / 'calculator_buttons.feature', self)

    def test_addition(self):
        """ Addition feature """
        verify(self.FEATURE_DIR / 'add_calculator.feature', self)

    def test_division(self):
        """ Division feature """
        verify(self.FEATURE_DIR / 'divide_calculator.feature', self)

    # Morelia automated steps
    # =======================

    # Given/Background Steps: Given the system state is known.

    def step_the_Calculator_is_powered_on(self):
        r"""the Calculator is powered on"""
        while not self.calculator.is_power_on:
            self.calculator.click_power()

    def step_the_Calculator_is_powered_off(self):
        r"""the Calculator is powered off"""
        while self.calculator.is_power_on:
            self.calculator.click_power()

    def step_the_Calculator_is_not_in_the_error_state(self):
        r'the Calculator is not in the error state'
        self.calculator.clear_error()

    # Error State Steps

    def step_the_calculator_goes_to_the_value_error_state(self):
        r'the calculator goes to the value error state'
        self.assertTrue(self.calculator.error_state)

    # Calculator Button Steps

    def step_I_press_the_calculator_clear_memory_button(self):
        r'I press the calculator clear memory button'
        self.calculator.clear_memory()

    def step_I_press_the_calculator_power_button(self):
        r'I press the calculator power button'
        self.calculator.click_power()

    def step_I_save_number_to_the_memory(self, number):
        r"""I save "([^"]+)" to the memory"""
        self.calculator.set_memory(float(number))

    def step_the_memory_value_is_zero(self):
        r"""the memory value is zero"""
        zero = 0.0
        self.assertEqual(self.calculator.memory, zero)

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

    def step_I_try_to_divide_by_zero(self):
        r'I try to divide by zero'
        self.calculator.divide(5.0, 0)


if __name__ == '__main__':
    unittest.main()
