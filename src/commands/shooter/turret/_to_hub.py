import warnings

import wpimath.geometry

import subsystems

from ._to_field_angle import ToFieldAngle


class ToHub(ToFieldAngle):
    class FieldRelativeAngleOverride(RuntimeWarning): pass

    def __init__(self):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', category=ToHub.FieldRelativeAngleOverride)
            super().__init__(wpimath.geometry.Rotation2d(0))
    
        self.setName('Turret To Hub')

    @property
    def _field_relative_angle(self):
        if subsystems.limelight.tv:
            self._field_relative_angle_ = self._pose_supplier().rotation().degrees() - subsystems.limelight.tx
        return self._field_relative_angle_

    @_field_relative_angle.setter
    def _field_relative_angle(self, value):
        warnings.warn("Cannot set TurretToHub's field relative angle", ToHub.FieldRelativeAngleOverride)
