import commands2

import constants
import subsystems

from ._set_speed import SetSpeed


class Callibrate(commands2.SequentialCommandGroup):
    def set_cw_val(self):
        self.cw_encoder_counts = subsystems.shooter.turret.get_raw_position()
    def set_ccw_val(self):
        self.ccw_encoder_counts = subsystems.shooter.turret.get_raw_position()

    def __init__(self) -> None:
        commands2.SequentialCommandGroup.__init__(
            [
                commands2.InstantCommand(subsystems.shooter.turret.set_speed(-0.5)),
                commands2.WaitCommand(10),
            ]
        )
        self.setName("Callibrate Turret")

    def end(self, interrupted: bool) -> None:
        subsystems.shooter.turret.set_speed(0)
        super().end()
