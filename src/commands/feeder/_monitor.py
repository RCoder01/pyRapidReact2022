import commands2

from commands.feeder._elevate_ball import ElevateBall
from commands.feeder._set_inactive import SetInactive
import subsystems
import utils.commands


class Monitor(utils.commands.RepeatCommand):
    def __init__(self) -> None:
        super().__init__(
            commands2.ConditionalCommand(
                ElevateBall(),
                SetInactive(),
                subsystems.feeder.get_in_sensor
            )
        )
        self.addRequirements(subsystems.feeder)
        self.setName("Feeder Monitor")
