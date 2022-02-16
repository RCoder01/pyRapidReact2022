import typing
import warnings

import wpimath.geometry

import utils.math

import constants
import subsystems

from ._to_robot_angle import ToRobotAngle


class ToFieldAngle(ToRobotAngle):
    class SetpointOverrideWarning(RuntimeWarning): pass

    def __init__(self, angle: wpimath.geometry.Rotation2d = wpimath.geometry.Rotation2d()) -> None:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', category=ToFieldAngle.SetpointOverrideWarning)
            super().__init__(angle)

        self.setName('Turret To Field Angle')

        self._pose_supplier = subsystems.drivetrain.get_pose

        self._heading_feed_forward = utils.math.HeadingFeedForward(
            constants.Shooter.Turret.FeedForward.H,
            self._pose_supplier()
        )

        self._field_relative_angle = angle

    @property
    def _setpoint(self):
        return (self._pose_supplier().rotation() - self._field_relative_angle).degrees()

    @_setpoint.setter
    def _setpoint(self, value: typing.Any):
        warnings.warn("Cannot set TurretToFieldAngle's setpoint", ToFieldAngle.SetpointOverrideWarning)

    def calculate_output(self) -> float:
        return super().calculate_output() + self._heading_feed_forward(self._pose_supplier())
