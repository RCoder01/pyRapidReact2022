import typing
import warnings

import wpimath.controller

import utils.warnings
import utils.constants

import subsystems

from ._set_speed import SetSpeed


class SetVariableSpeed(SetSpeed):
    class SpeedSetpointOverrideWarning(utils.warnings.SetpointOverrideWarning): pass

    def __init__(
            self,
            josh: subsystems.shooter._josh.Josh,
            speed_supplier: typing.Callable[[], float],
            ) -> None:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=self.SpeedSetpointOverrideWarning)
            super().__init__(josh, 0)
        self.setName(f"Set {josh.getName()} Variable Speed")

        self._speed_supplier = speed_supplier

    @property
    def _speed_setpoint(self):
        return self._speed_supplier()

    @_speed_setpoint.setter
    def _speed_setpoint(self, value):
        warnings.warn("Josh SetVariableSpeed's _speed_setpoint is read-only", self.SpeedSetpointOverrideWarning)
