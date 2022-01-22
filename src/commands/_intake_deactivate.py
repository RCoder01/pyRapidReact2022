import commands2

import constants
import subsystems


class DeactivateIntake(commands2.InstantCommand):

    def __init__(self) -> None:
        super().addRequirements(subsystems.intake)

    def execute(self):
        subsystems.intake.set_speed(0)

    def isFinished(self) -> bool:
        return True