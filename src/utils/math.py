from __future__ import annotations

import wpimath.geometry

class HeadingFeedForward:
    def __init__(self, kP=1, last_robot_position: wpimath.geometry.Pose2d = wpimath.geometry.Pose2d()) -> None:
        self._kP = kP
        self._last_robot_position = last_robot_position

    def __call__(self, robot_position: wpimath.geometry.Pose2d) -> float:
        """Extrapolate past and current robot positions to calculate natural change in field-relative angle."""
        return (
            robot_position.relativeTo(robot_position.exp(self._last_robot_position.log(robot_position))).rotation().degrees() \
            - robot_position.rotation().degrees() \
            * self._kP
        )
    
    def calculate(self, robot_position: wpimath.geometry.Pose2d) -> float:
        """Extrapolate past and current robot positions to calculate natural change in field-relative angle."""
        return self(robot_position)

# TODO: Add vector3D