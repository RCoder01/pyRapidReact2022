import math
import warnings

import wpimath.geometry
import constants
import subsystems
import utils.math
from ._turret_to_robot_angle import TurretToRobotAngle


class TurretToFieldAngle(TurretToRobotAngle):
    class SetpointOverrideWarning(RuntimeWarning): pass

    def __init__(self, angle: float = 0) -> None:
        super().__init__(angle)
        self.setName('Turret To Field Angle')

        self._pose_supplier = subsystems.drivetrain.get_pose
        self._heading_feed_forward = utils.math.HeadingFeedForward(
            constants.Shooter.Turret.FeedForward.H,
            self._pose_supplier()
        )

    @property
    def _setpoint(self):
        if subsystems.limelight.tv:
            return subsystems.shooter.turret.get_angle() + subsystems.limelight.tx
        else:
            pose = self._pose_supplier()
            translation = pose.translation()
            hub_angle = wpimath.geometry.Rotation2d(-translation.x, -translation.y)
            return (pose.rotation() - hub_angle).degrees()

    @_setpoint.setter
    def _setpoint(self, value):
        warnings.warn("Cannot set TurretToFieldAngle's setpoint", TurretToFieldAngle.SetpointOverrideWarning)

    def calculate_output(self) -> float:
        return super().calculate_output() + self._heading_feed_forward(self._pose_supplier())
