import enum
import typing

import wpilib


class SingleDigitalInput(wpilib.DigitalInput):
    def __init__(self, channel: int, inverted: bool) -> None:
        super().__init__(channel)
        self._INVERTED = inverted
    
    def get(self):
        return super().get() ^ self._INVERTED


class DoubleDigitialInput(SingleDigitalInput):
    def __init__(self, primary_ID: int, secondary_ID: int, primary_inverted: bool, secondary_inverted: bool):
        super().__init__(primary_ID, primary_inverted)
        self._secondary = SingleDigitalInput(secondary_ID, secondary_inverted)
        self.config_default_get(self.get_primary)

    def config_default_get(self, method: typing.Callable[[], bool]):
        self._default_get = method

    def get(self):
        return self._default_get()

    def get_primary(self):
        return super().get()

    def get_secondary(self):
        return self._secondary.get()

    def get_leniant(self):
        return self.get_primary() or self.get_secondary()

    def get_strict(self):
        return self.get_primary() and self.get_secondary()

    def in_error_state(self):
        return self.get_leniant() and not self.get_strict()
