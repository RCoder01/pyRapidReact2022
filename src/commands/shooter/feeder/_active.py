from re import sub
import commands2

import subsystems
import constants


class Active(commands2.CommandBase):
    def __init__(self, speed: float = constants.Shooter.Feeder.DEFAULT_SPEED):
        commands2.CommandBase.__init__(self)
        self.addRequirements(subsystems.shooter.feeder)

        self._speed = speed

    def initialize(self) -> None:
        subsystems.shooter.feeder.set_speed(self._speed)
        return super().initialize()

    def end(self, interrupted: bool) -> None:
        subsystems.shooter.feeder.set_speed(0)
        return super().end(interrupted)
