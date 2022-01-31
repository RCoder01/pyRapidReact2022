import commands2

import subsystems


class DriveStraight(commands2.CommandBase):
    """Drive straight for a certain distance"""

    def __init__(self, speed: float, distance: float, tolerance: float = 0) -> None:
        commands2.CommandBase.__init__(self)
        self.addRequirements(subsystems.drivetrain)
        self.setName("DriveStraight")

        self._speed = speed
        self._distance = distance
        self._tolerance = tolerance

        subsystems.drivetrain.set_speed(
            self._speed,
            self._speed,
        )

    def isFinished(self) -> None:
        return subsystems.drivetrain.get_left_encoder_position() >= self._distance - self._tolerance and \
               subsystems.drivetrain.get_right_encoder_position() >= self._distance - self._tolerance
