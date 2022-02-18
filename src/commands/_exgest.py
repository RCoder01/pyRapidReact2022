import commands2
from wpilib import SmartDashboard

import commands
import constants


class Exgest(commands2.ParallelCommandGroup):
    def __init__(self):
        commands2.ParallelCommandGroup.__init__(
            self,
            commands.intake.SetActive(constants.Intake.DEFAULT_EXGEST_SPEED),
            commands.feeder.SetActive(
                constants.Feeder.TopMotors.DEFAULT_EXGEST_SPEED,
                constants.Feeder.BottomMotors.DEFAULT_EXGEST_SPEED
            ),
        )
        self.setName("Exgest")

    def isFinished(self) -> bool:
        return SmartDashboard.getNumber("Stored Balls", 1) <= 0

    def end(self, interrupted: bool) -> None:
        commands.intake.SetInactive().schedule()
        commands.feeder.SetInactive().schedule()
        super().end(interrupted)
