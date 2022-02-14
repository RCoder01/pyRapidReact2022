import commands2

import subsystems


class SetInactive(commands2.InstantCommand):
    """Deactivates the intake (sets speed to 0)."""

    def __init__(self) -> None:
        commands2.InstantCommand.__init__(self)
        self.addRequirements(subsystems.intake)
        self.setName("Set Intake Inactive")

    def initialize(self) -> None:
        subsystems.intake.set_speed(0)
        subsystems.intake.set_active(False)

        super().execute()