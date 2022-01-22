import commands2

import subsystems


class DriveStraight(commands2.CommandBase):

    def __init__(self, speed: float, distance: float, tolerance: float = 0) -> None:
        super().addRequirements(subsystems.drivetrain)

        self._speed = speed
        self._distance = distance
        self._tolerance = tolerance

        subsystems.drivetrain.set_speed(
            self._speed,
            self._speed,
        )

    def end(self, interrupted: bool) -> None:
        return subsystems.drivetrain.get_left_encoder_position() >= self._distance - self._tolerance and \
               subsystems.drivetrain.get_right_encoder_position() >= self._distance - self._tolerance