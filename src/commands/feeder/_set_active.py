import commands2

import constants
import subsystems


class SetActive(commands2.InstantCommand):
    """Activates the feeder at a given/default speed."""

    def __init__(
            self,
            top_speed: float = constants.Feeder.TopMotors.DEFAULT_SPEED,
            bottom_speed: float = constants.Feeder.BottomMotors.DEFAULT_SPEED
            ) -> None:
        commands2.InstantCommand.__init__(self)
        self.addRequirements(subsystems.feeder)
        self.setName("Set Intake Active")

        self._top_speed = top_speed
        self._bottom_speed = bottom_speed

    def initialize(self) -> None:
        subsystems.feeder.set_speeds(self._top_speed, self._bottom_speed)

        super().execute()
