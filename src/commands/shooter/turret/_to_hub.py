import warnings

import wpimath.geometry

import utils.warnings

import subsystems

from ._to_field_angle import ToFieldAngle


class ToHub(ToFieldAngle):
    class FieldRelativeAngleOverride(utils.warnings.SetpointOverrideWarning): pass

    def __init__(self):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', category=self.FieldRelativeAngleOverride)
            super().__init__(wpimath.geometry.Rotation2d(0))
    
        self.setName('Turret To Hub')

    @property
    def _field_relative_angle(self):
        pose = self._pose_supplier()
        if subsystems.limelight.tv:
            return pose.rotation().degrees() - (subsystems.limelight.tx + subsystems.shooter.turret.get_angle())
        translation = pose.translation()
        return wpimath.geometry.Rotation2d(-translation.x, -translation.y).degrees()

    @_field_relative_angle.setter
    def _field_relative_angle(self, value):
        warnings.warn("Field relative angle setpoint is read-only", self.FieldRelativeAngleOverride)
