import commands2
import wpimath.filter

import utils.commands
import constants

from commands.belt._elevate_ball import ElevateBall
import subsystems


class Monitor(utils.commands.RepeatCommand):
    def __init__(self) -> None:
        self._in_debouncer = wpimath.filter.Debouncer(constants.Belt.IN_SENSOR_DEBOUNCE_TIME)
        self._get_debounced_in = lambda: self._in_debouncer.calculate(subsystems.belt.get_in_sensor())
        self._out_debouncer = wpimath.filter.Debouncer(constants.Belt.OUT_SENSOR_DEBOUNCE_TIME)
        self._get_debounced_out = lambda: self._out_debouncer.calculate(subsystems.belt.get_out_sensor())
        super().__init__(
            commands2.SequentialCommandGroup(
                commands2.WaitUntilCommand(
                    lambda: (
                        self._in_debouncer.calculate(subsystems.belt.get_in_sensor()) and
                        not self._out_debouncer.calculate(subsystems.belt.get_out_sensor())
                    )
                ),
                ElevateBall(),
            )
        )
        self.setName("Belt Monitor")
