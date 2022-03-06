import warnings
import commands2

import constants
import subsystems


class Callibrate(commands2.CommandBase):
    def __init__(self) -> None:
        commands2.CommandBase.__init__(self)
        self.setName("Callibrate Turret")

    def initialize(self) -> None:
        subsystems.shooter.turret.set_callibration_status(subsystems.shooter.turret.CallibrationStatus.CALLIBRATING)
        subsystems.shooter.turret.config_max_speed(constants.Shooter.Turret.CALLIBRATION_SPEED)
        subsystems.shooter.turret.set_speed(constants.Shooter.Turret.CALLIBRATION_SPEED)
        subsystems.shooter.turret.set_reverse_soft_limit(False)

    def isFinished(self) -> bool:
        return subsystems.shooter.turret.get_reverse_limit_switch()

    def end(self, interrupted: bool) -> None:
        subsystems.shooter.turret.set_speed(0)

        if interrupted:
            subsystems.shooter.turret.set_callibration_status(subsystems.shooter.turret.CallibrationStatus.NEEDS_CALLIBRATION)
            subsystems.shooter.turret.config_max_speed(0)
            warnings.warn("Callibration interrupted!", RuntimeWarning)
        else:
            subsystems.shooter.turret.set_callibration_status(subsystems.shooter.turret.CallibrationStatus.CALLIBRATED)
            subsystems.shooter.turret.set_forward_soft_limit(True)
            subsystems.shooter.turret.config_max_speed(constants.Shooter.Turret.STANDARD_TOP_SPEED)
            subsystems.shooter.turret.set_soft_offset(constants.Shooter.Turret.ANGLE_MIN_DEGREES * constants.Shooter.Turret.ENCODER_COUNTS_PER_DEGREE)
        return super().end(interrupted)
