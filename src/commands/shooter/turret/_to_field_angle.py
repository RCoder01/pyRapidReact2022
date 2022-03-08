import typing
import warnings
import wpilib

import wpimath.geometry

import utils.math

import constants
import subsystems

from ._to_robot_angle import ToRobotAngle


class ToFieldAngle(ToRobotAngle):
    class SetpointOverrideWarning(utils.warnings.SetpointOverrideWarning): pass

    def __init__(self, angle: wpimath.geometry.Rotation2d = wpimath.geometry.Rotation2d()) -> None:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', category=self.SetpointOverrideWarning)
            super().__init__(angle)

        self.setName('Turret To Field Angle')

        self._pose_supplier = subsystems.drivetrain.get_pose

        # self._heading_feed_forward = lambda: (subsystems.drivetrain.get_turn_rate() * constants.Shooter.Turret.HeadingFeedForward)
        # self._heading_feed_forward = utils.math.HeadingFeedForward(
        #     constants.Shooter.Turret.HeadingFeedForward,
        #     self._pose_supplier()
        # )

        self._field_relative_angle = angle

    def execute(self) -> None:
        wpilib.SmartDashboard.putNumber('Turret/Field Angle Setpoint', self._field_relative_angle.degrees())
        return super().execute()

    @property
    def _setpoint(self):
        return (self._pose_supplier().rotation() - self._field_relative_angle).degrees()

    @_setpoint.setter
    def _setpoint(self, value: typing.Any):
        warnings.warn("TurretToFieldAngle's setpoint is read-only", self.SetpointOverrideWarning)
