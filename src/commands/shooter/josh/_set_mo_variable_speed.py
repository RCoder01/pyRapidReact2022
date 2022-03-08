import typing

import wpimath.controller

import constants
import subsystems

from ._set_variable_speed import SetVariableSpeed


class SetMoVariableSpeed(SetVariableSpeed):
    def __init__(self, speed_supplier: typing.Callable[[], float]) -> None:
        super().__init__(
            subsystems.shooter.mo,
            speed_supplier,
        )
