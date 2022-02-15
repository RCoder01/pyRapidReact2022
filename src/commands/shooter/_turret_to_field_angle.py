import constants
import subsystems
import utils.math
from ._turret_to_robot_angle import TurretToRobotAngle


class TurretToFieldAngle(TurretToRobotAngle):
    def __init__(self, angle: float) -> None:
        super().__init__(angle)
        self.setName('Turret To Field Angle')

        self._angle_supplier = lambda: subsystems.limelight.tx
        self._pose_supplier = subsystems.drivetrain.get_pose
        self._heading_feed_forward = utils.math.HeadingFeedForward(
            constants.Shooter.Turret.FeedForward.H,
            self._pose_supplier()
        )

    @property
    def _setpoint(self):
        return super()._setpoint + self._angle_supplier()

    def calculate_output(self) -> float:
        output = super().calculate_output()
        output += self._heading_feed_forward(self._angle_supplier())
        return output
