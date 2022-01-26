import commands2
import wpilib

import subsystems
import constants


class IntakeActivate(commands2.InstantCommand):
    """Activates the intake at a given/default speed."""

    def __init__(self, speed: float = constants.Intake.DEFAULT_INTAKE_SPEED):
        self.__init__()
        self.addRequirements(subsystems.intake)
        self.setName("ActivateIntake")

        self._speed = speed

    
    def execute(self):
        subsystems.intake.set_speed(self._speed)
        wpilib.SmartDashboard.putBoolean("Intake Active", True)

        self.execute()
    
    def isFinished(self) -> bool:
        return True