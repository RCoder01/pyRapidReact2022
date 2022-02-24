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
            wpimath.controller.PIDController(
                constants.Shooter.Josh.Lester.PID.Kp,
                constants.Shooter.Josh.Lester.PID.Ki,
                constants.Shooter.Josh.Lester.PID.Kd,
            ),
            constants.Shooter.Josh.Lester.FeedForward,
            constants.Shooter.Josh.Lester.PIDTolerance,
        )
