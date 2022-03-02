import sched
import commands2
from wpilib import SmartDashboard

import commands
import constants


class Exgest(commands2.ParallelDeadlineGroup):
    def __init__(self):
        commands2.ParallelDeadlineGroup.__init__(
            self,
            commands2.ParallelRaceGroup(
                commands2.WaitCommand(constants.Misc.EXGEST_TIMEOUT),
                commands2.WaitUntilCommand(lambda: SmartDashboard.getNumber("Stored Balls", 1) <= -1), #TODO: Revert -1 to 0
            ),
            [
                commands2.ParallelCommandGroup(
                    [
                        commands.intake.Active(constants.Intake.DEFAULT_EXGEST_SPEED),
                        commands.belt.Active(
                            constants.Belt.DEFAULT_EXGEST_SPEED,
                        ),
                    ]
                ),
            ]
        )
        self.setName("Exgest")
