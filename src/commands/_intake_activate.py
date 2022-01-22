import commands2

import subsystems
import constants


class ActivateIntake(commands2.InstantCommand):

    def __init__(self, speed: float = constants.IntakeConstants.DEFAULT_INTAKE_SPEED):
        super().addRequirements(subsystems.intake)
        self._speed = speed
    
    def execute(self):
        subsystems.intake.set_speed(self._speed)
    
    def isFinished(self) -> bool:
        return True