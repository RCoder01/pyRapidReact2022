import commands2
import wpimath.controller

import constants
import subsystems


class DriveStraight(commands2.Command):

    def getRequirements(self) -> set[commands2.Subsystem]:
        return {subsystems.drivetrain}

    def __init__(self, speed: float, distance: float):
        self._speed = speed
        self._distance = distance

    def execute(self) -> None:
        subsystems.drivetrain.set_speed(
            self._speed,
            self._speed,
        )