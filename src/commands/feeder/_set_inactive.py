import commands2
import wpilib

import subsystems


class SetInactive(commands2.InstantCommand):
    """Deactivates the feeder (sets speed to 0)."""

    def __init__(self) -> None:
        commands2.InstantCommand.__init__(self)
        self.addRequirements(subsystems.feeder)
        self.setName("Set Feeder Inactive")

    def initialize(self) -> None:
        subsystems.feeder.set_speeds(0)
        wpilib.SmartDashboard.putBoolean("Feeder Active", False)

        super().execute()
