import typing

import wpimath.controller

import constants
import subsystems

from ._set_variable_speed import SetVariableSpeed


class SetLesterSpeed(SetVariableSpeed):
    def __init__(self, speed_supplier: typing.Callable[[], float]) -> None:
        super().__init__(
            subsystems.shooter.mo,
            speed_supplier,
            wpimath.controller.PIDController(
                constants.Shooter.Josh.Lester.PID.P,
                constants.Shooter.Josh.Lester.PID.I,
                constants.Shooter.Josh.Lester.PID.D,
            ),
            constants.Shooter.Josh.Lester.FeedForward,
            constants.Shooter.Josh.Lester.PID.SetpointTolerance,
        )
