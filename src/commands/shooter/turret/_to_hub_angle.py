import warnings
import wpilib

import wpimath.geometry

import utils.warnings

import subsystems

from ._to_field_angle import ToFieldAngle


class ToHubAngle(ToFieldAngle):
    class FieldRelativeAngleOverride(utils.warnings.SetpointOverrideWarning): pass

    def __init__(self, hub_angle = 0):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', category=self.FieldRelativeAngleOverride)
            super().__init__(wpimath.geometry.Rotation2d(0))

        self.setName('Turret To Hub Angle')

        self._hub_angle = hub_angle

    def execute(self) -> None:
        wpilib.SmartDashboard.putNumber('Turret/Field Angle Setpoint', self._field_relative_angle)
        return super().execute()

    @property
    def _field_relative_angle(self):
        pose = self._pose_supplier()
        if subsystems.limelight.tv:
            self._last_hub_field_position = \
                pose.translation() \
              + wpimath.geometry.Translation2d(
                    subsystems.limelight.distance,
                    wpimath.geometry.Rotation2d(subsystems.limelight.tx)
                  + subsystems.shooter.turret.get_robot_relative_rotation()
                  + pose.rotation()
                )
            wpilib.SmartDashboard.putData(self._last_hub_field_position)
            return pose.rotation().degrees() - ((subsystems.limelight.tx - self._hub_angle) + subsystems.shooter.turret.get_angle())
        translation = pose.translation()
        return wpimath.geometry.Rotation2d(-translation.x, -translation.y).degrees()

    @_field_relative_angle.setter
    def _field_relative_angle(self, value):
        warnings.warn("Field relative angle setpoint is read-only", self.FieldRelativeAngleOverride)
