import commands2
import wpilib

import subsystems
import constants


class Active(commands2.CommandBase):
    def __init__(self, speed: float = constants.Intake.DEFAULT_INTAKE_SPEED):
        commands2.CommandBase.__init__(self)
        self.addRequirements(subsystems.intake)
        self.setName("Intake Active")

        self._speed = speed

    def initialize(self) -> None:
        subsystems.intake.set_speed(self._speed)
        wpilib.SmartDashboard.putBoolean("Intake Active", True)

    def end(self, interrupted: bool) -> None:
        subsystems.intake.set_speed(0)
        wpilib.SmartDashboard.putBoolean("Intake Active", False)
        super().end(interrupted)
