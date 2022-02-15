import subsystems

from ._turret_to_robot_angle import TurretToRobotAngle


class TurretToFieldAngle(TurretToRobotAngle):
    def __init__(self, angle: float) -> None:
        super().__init__(angle)
        self.setName('Turret To Field Angle')

    @property
    def _setpoint(self):
        return super()._setpoint + subsystems.limelight.tx

    def calculate_output(self) -> float:
        return super().calculate_output()
