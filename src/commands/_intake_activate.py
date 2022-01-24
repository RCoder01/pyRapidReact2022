import commands2
import wpilib

import subsystems
import constants


class IntakeActivate(commands2.InstantCommand):
    """Activates the intake at a given/default speed."""

    def __init__(self, speed: float = constants.IntakeConstants.DEFAULT_INTAKE_SPEED):
        super().addRequirements(subsystems.intake)
        super().setName("ActivateIntake")

        self._speed = speed

        super().__init__()
    
    def execute(self):
        subsystems.intake.set_speed(self._speed)
        wpilib.SmartDashboard.putBoolean("Intake Active", True)

        super().execute()
    
    def isFinished(self) -> bool:
        return True