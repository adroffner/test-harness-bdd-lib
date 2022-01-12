
class CalculatorPoweredOff(Exception):
    pass


class Calculator:
    """ Calculator Simulation

    Simulate a desk calculator.
    """

    def __init__(self):
        self._is_on = False
        self._memory = 0.0
        self._error_state = False

    @property
    def is_power_on(self):
        return self._is_on

    def click_power(self):
        if self.is_power_on:
            self.clear_memory()
        self._is_on = not self._is_on

    def clear_memory(self):
        self._memory = 0.0

    def set_memory(self, value):
        if self.is_power_on:
            self._memory = value
        else:
            raise CalculatorPoweredOff(f'cannot set memory to {value}')

    @property
    def memory(self):
        return self._memory

    def clear_error(self):
        self._error_state = False

    @property
    def error_state(self):
        return self._error_state

    def add(self, a, b):
        if self.is_power_on:
            return a + b
        else:
            raise CalculatorPoweredOff(f'cannot add {a} + {b}')

    def divide(self, a, b):
        if self.is_power_on:
            try:
                return a / b
            except (ValueError, ZeroDivisionError):
                self._error_state = True
        else:
            raise CalculatorPoweredOff(f'cannot divide {a} / {b}')
