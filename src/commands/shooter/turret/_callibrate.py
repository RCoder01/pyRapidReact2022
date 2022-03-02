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
        speed_direction = 1 if constants.Shooter.Turret.POSITIVE_SPEED_CLOCKWISE else -1
        commands2.SequentialCommandGroup.__init__(
            self,
            [
                SetSpeed(speed_direction * constants.Shooter.Turret.CALIBRATION_SPEED).until(subsystems.shooter.turret.get_cw_limit_switch),
                commands2.InstantCommand(self.set_cw_val),
                SetSpeed(-speed_direction * constants.Shooter.Turret.CALIBRATION_SPEED).until(subsystems.shooter.turret.get_ccw_limit_switch()),
                commands2.InstantCommand(self.set_ccw_val),
                SetSpeed(speed_direction * constants.Shooter.Turret.CALIBRATION_SPEED).until(
                        lambda: speed_direction * subsystems.shooter.turret.get_raw_position() > 
                            (speed_direction * (self.cw_encoder_counts + self.ccw_encoder_counts) / 2)
                    )
            ]
        )
        self.setName("Callibrate Turret")

    def end(self, interrupted: bool) -> None:
        subsystems.shooter.turret._motors.configure_units(
            (self.cw_encoder_counts - self.ccw_encoder_counts)
             / (constants.Shooter.Turret.ANGLE_MAX_DEGREES - constants.Shooter.Turret.ANGLE_MIN_DEGREES)
        )
        subsystems.shooter.turret._motors.reset_lead_encoder_position()
