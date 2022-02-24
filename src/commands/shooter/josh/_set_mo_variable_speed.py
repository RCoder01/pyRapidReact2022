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
            wpimath.controller.PIDController(
                constants.Shooter.Josh.Mo.PID.Kp,
                constants.Shooter.Josh.Mo.PID.Ki,
                constants.Shooter.Josh.Mo.PID.Kd,
            ),
            constants.Shooter.Josh.Mo.FeedForward,
            constants.Shooter.Josh.Mo.PIDTolerance,
        )
