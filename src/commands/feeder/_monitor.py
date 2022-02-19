import commands2

import utils.commands

from commands.feeder._elevate_ball import ElevateBall
from commands.feeder._set_inactive import SetInactive
import subsystems


class Monitor(utils.commands.RepeatCommand):
    def __init__(self) -> None:
        super().__init__(
            commands2.ConditionalCommand(
                ElevateBall(),
                SetInactive(),
                subsystems.feeder.get_in_sensor
            )
        )
        # self.addRequirements(subsystems.feeder)
        self.setName("Feeder Monitor")
