import commands2
import wpilib

import constants
import subsystems


class IntakeDeactivate(commands2.InstantCommand):
    """Deactivates the intake (sets speed to 0)."""

    def __init__(self) -> None:
        self.__init__()
        self.addRequirements(subsystems.intake)
        self.setName("DeactivateIntake")

    def execute(self):
        subsystems.intake.set_speed(0)
        wpilib.SmartDashboard.putBoolean("Intake Active", False)

        self.execute()

    def isFinished(self) -> bool:
        return True