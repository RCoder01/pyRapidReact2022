import commands2

import subsystems


class DriveStraight(commands2.CommandBase):
    """Drive straight for a certain distance"""

    def __init__(self, speed: float, distance: float, tolerance: float = 0) -> None:
        self.__init__()
        self.addRequirements(subsystems.drivetrain)
        self.setName("DriveStraight")

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