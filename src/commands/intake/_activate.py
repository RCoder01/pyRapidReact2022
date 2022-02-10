import commands2
import wpilib

import subsystems
import constants


class Activate(commands2.InstantCommand):
    """Activates the intake at a given/default speed."""

    def __init__(self, speed: float = constants.Intake.DEFAULT_INTAKE_SPEED):
        commands2.InstantCommand.__init__(self)
        self.addRequirements(subsystems.intake)
        self.setName("ActivateIntake")

        self._speed = speed
    
    def execute(self):
        subsystems.intake.set_speed(self._speed)
        wpilib.SmartDashboard.putBoolean("Intake Active", True)

        super().execute()
    
    def isFinished(self) -> bool:
        return True
