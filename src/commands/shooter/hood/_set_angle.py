import commands2

import subsystems


class SetAngle(commands2.CommandBase):
    def __init__(self, angle: float) -> None:
        commands2.CommandBase.__init__(self)
        self.addRequirements(subsystems.shooter.hood)
        self.setName(f"Set Hood Angle")

        self._angle_setpoint = angle

    def execute(self) -> None:
        subsystems.shooter.hood.set_angle(self._angle_setpoint)
        return super().execute()

    def end(self, interrupted: bool) -> None:
        self._josh.set_output(0)
        return super().end(interrupted)
