import typing

import wpimath.controller

import constants
import subsystems

from ._set_variable_speed import SetVariableSpeed


class SetLesterVariableSpeed(SetVariableSpeed):
    def __init__(self, speed_supplier: typing.Callable[[], float]) -> None:
        super().__init__(
            subsystems.shooter.lester,
            speed_supplier,
        )
