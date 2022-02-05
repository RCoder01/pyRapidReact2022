import typing
import commands2
from wpilib import SmartDashboard

import utils


class Turret(commands2.SubsystemBase):

    def periodic(self) -> None:
        SmartDashboard.putNumber('Turret Encoder', self.get_encoder_value())

    def __init__(self, motor_IDs: typing.Collection[int], continuous_max_cumulative_encoder_counts: int):
        commands2.SubsystemBase.__init__(self)

        self._CONTINUOUS_MAX_CUMULATIVE_ENCODER_COUNTS = continuous_max_cumulative_encoder_counts
        self._motors = utils.ContinuousHeadedDefaultMotorGroup(motor_IDs, continuous_max_cumulative_encoder_counts=continuous_max_cumulative_encoder_counts)

    def set_speed(self, speed: float):
        self._motors.set_speed(speed)

    def get_cumulative_encoder(self):
        return self._motors.get_cumulative_distance()

    def get_angle(self):
        return self.get_cumulative_encoder / self._CONTINUOUS_MAX_CUMULATIVE_ENCODER_COUNTS * 360
