import commands2
from wpilib import SmartDashboard

import commands
import constants
import subsystems


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

        self._set_intake_inactive_command = commands.intake.SetInactive()
        self._set_feeder_inactive_command = commands.feeder.SetInactive()

    def isFinished(self) -> bool:
        return False # SmartDashboard.getNumber("Stored Balls", 1) <= 0

    def end(self, interrupted: bool) -> None:
        commands2.InstantCommand(lambda: subsystems.intake._motors.set_output(0)).schedule()
        commands2.InstantCommand(lambda: (subsystems.feeder._bottom_motor_group.set_output(0), subsystems.feeder._top_motor_group.set_output(0))).schedule()

        # self._set_intake_inactive_command.schedule()
        # self._set_feeder_inactive_command.schedule()
        super().end(interrupted)
