import commands2

import constants
import subsystems

from ._active import Active


class ElevateBall(commands2.ConditionalCommand):
    def __init__(self) -> None:
        commands2.ConditionalCommand.__init__(
            self,
            # commands2.ParallelDeadlineGroup(
            #     commands2.WaitCommand(constants.Belt.STAGING_RUN_TIME),
            #     [Active()],
            # ),
            commands2.InstantCommand(),
            Active().until(subsystems.belt.get_out_sensor).withTimeout(constants.Belt.TIMEOUT),
            subsystems.belt.get_out_sensor
        )
        self.setName("Belt Elevate Ball")
