import typing
import warnings

import utils.warnings
import utils.constants

import subsystems

from ._set_angle import SetAngle


class SetVariableAngle(SetAngle):
    class AngleSetpointOverrideWarning(utils.warnings.SetpointOverrideWarning): pass

    def __init__(self, angle_supplier: typing.Callable[[], float]) -> None:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=self.AngleSetpointOverrideWarning)
            super().__init__(0)
        self.setName(f"Set Hood Variable Angle")

        self._angle_supplier = angle_supplier

    @property
    def _angle_setpoint(self):
        return self._angle_supplier()

    @_angle_setpoint.setter
    def _angle_setpoint(self, value):
        warnings.warn("Josh SetVariableSpeed's _angle_setpoint is read-only", self.AngleSetpointOverrideWarning)
