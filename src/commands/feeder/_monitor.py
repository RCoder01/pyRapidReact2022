import commands2

from commands.feeder._set_active import SetActive
from commands.feeder._set_inactive import SetInactive
import subsystems
import utils.commands


@utils.commands.RepeatCommand
class Monitor(commands2.CommandBase):
    def __init__(self) -> None:
        commands2.CommandBase.__init__(self)
        self.addRequirements(subsystems.feeder)
        self.setName("Feeder Monitor")

        self._activate = SetActive().initialize
        self._deactivate = SetInactive().initialize

    def initialize(self) -> None:
        self._deactivate()

    def execute(self) -> None:
        if subsystems.feeder.get_out_sensor():
            self._deactivate()
        elif subsystems.feeder.get_in_sensor():
            self._activate()

    def isFinished(self) -> bool:
        return False

    def end(self, interrupted: bool) -> None:
        self._deactivate()
        return super().end(interrupted)
