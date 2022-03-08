import typing
import commands2
import wpimath.controller

import subsystems

import utils.constants


class SetSpeed(commands2.CommandBase):
    def __init__(
            self,
            josh: subsystems.shooter._josh.Josh,
            speed: float,
            ) -> None:
        commands2.CommandBase.__init__(self)
        self.addRequirements(josh)
        self.setName(f"Set {josh.getName()} Speed")

        self._josh = josh

        self._speed_setpoint = speed

    def execute(self) -> None:
        self._josh.set_velocity_rpm(self._speed_setpoint)
        return super().execute()

    def end(self, interrupted: bool) -> None:
        self._josh.set_output(0)
        return super().end(interrupted)
