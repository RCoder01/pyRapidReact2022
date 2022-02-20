import commands2
import wpilib

import constants
import subsystems


class Active(commands2.CommandBase):
    def __init__(self, speed: float = constants.Belt.DEFAULT_SPEED) -> None:
        commands2.CommandBase.__init__(self)
        self.addRequirements(subsystems.belt)
        self.setName("Belt Active")

        self._speed = speed

    def initialize(self) -> None:
        subsystems.belt.set_speed(self._speed)
        wpilib.SmartDashboard.putBoolean("Belt Active", True)
        return super().initialize()

    def end(self, interrupted: bool) -> None:
        subsystems.belt.set_speed(0)
        wpilib.SmartDashboard.putBoolean("Belt Active", False)
        return super().end(interrupted)
