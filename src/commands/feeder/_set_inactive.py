import commands2

import subsystems


class SetInactive(commands2.InstantCommand):
    """Deactivates the intake (sets speed to 0)."""

    def __init__(self) -> None:
        commands2.InstantCommand.__init__(self)
        self.addRequirements(subsystems.feeder)
        self.setName("Set Feeder Inactive")

    def initialize(self) -> None:
        subsystems.feeder.set_speeds(0)

        super().execute()
