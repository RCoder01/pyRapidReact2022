import math

import wpimath.geometry

class HeadingFeedForward:
    def __init__(self, kP=1) -> None:
        self._kP = kP

    def __call__(self, last_robot_position: wpimath.geometry.Pose2d, robot_position: wpimath.geometry.Pose2d) -> float:
        """Extrapolate past and current robot positions to calculate natural change in field-relative angle."""
        return robot_position.relativeTo(robot_position.exp(last_robot_position.log(robot_position))).rotation().degrees() * self._kP

__all__ = [
    'HeadingFeedForward',
]
