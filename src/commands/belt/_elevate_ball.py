import commands2

import constants
import subsystems

from ._active import Active


class ElevateBall(commands2.ConditionalCommand):
    def __init__(self) -> None:
        super().__init__(
            commands2.ParallelDeadlineGroup(
                commands2.WaitCommand(constants.Belt.STAGING_RUN_TIME),
                Active(),
            ),
            Active().until(subsystems.belt.get_out_sensor),
            subsystems.belt.get_out_sensor
        )
        self.setName("Belt Elevate Ball")
