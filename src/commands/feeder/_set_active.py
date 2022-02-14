import commands2

import subsystems


class SetActive(commands2.InstantCommand):
    """Activates the feeder at a given/default speed."""

    def __init__(self, speed: float = subsystems.feeder.DEFAULT_INTAKE_SPEED) -> None:
        commands2.InstantCommand.__init__(self)
        self.addRequirements(subsystems.feeder)
        self.setName("Set Intake Active")

        self._speed = speed

    def initialize(self) -> None:
        subsystems.feeder.set_speed(self._speed)
        subsystems.feeder.set_active(True)

        super().execute()
