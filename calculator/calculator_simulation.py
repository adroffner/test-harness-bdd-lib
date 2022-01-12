
class CalculatorPoweredOff(Exception):
    pass


class Calculator:
    """ Calculator Simulation

    Simulate a desk calculator.
    """

    def __init__(self):
        self._is_on = False
        self._memory = 0.0

    @property
    def is_power_on(self):
        return self._is_on

    def click_power(self):
        self._is_on = not self._is_on

    def add(self, a, b):
        if self.is_power_on:
            return a + b
        else:
            raise CalculatorPoweredOff(f'cannot add {a} + {b}')
