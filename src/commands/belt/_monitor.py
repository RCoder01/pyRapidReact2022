import commands2
import wpimath.filter

import utils.commands
import constants

from commands.belt._elevate_ball import ElevateBall
import subsystems


class Monitor(utils.commands.RepeatCommand):
    def __init__(self) -> None:
        self._debouncer = wpimath.filter.Debouncer(constants.Belt.IN_SENSOR_DEBOUNCE_TIME)
        super().__init__(
            commands2.ConditionalCommand(
                commands2.SequentialCommandGroup(
                    ElevateBall(),
                    commands2.WaitUntilCommand(lambda: not self._debouncer.calculate(subsystems.belt.get_in_sensor()))
                ),
                commands2.WaitUntilCommand(lambda: True),
                lambda: self._debouncer.calculate(subsystems.belt.get_in_sensor())
            )
        )
        self.setName("Belt Monitor")
