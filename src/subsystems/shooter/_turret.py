import typing
import commands2
from wpilib import SmartDashboard

import utils.motor


class Turret(commands2.SubsystemBase):

    def periodic(self) -> None:
        SmartDashboard.putNumber('Turret Encoder', self.get_cumulative_encoder())
        # TODO: Sim stuff

    def __init__(self, motor_IDs: typing.Collection[int], total_cumulative_encoder_counts: int, angle_range_degrees: float):
        commands2.SubsystemBase.__init__(self)

        self._TOTAL_CUMULATIVE_ENCODER_COUNTS = total_cumulative_encoder_counts
        self._ANGLE_RANGE = angle_range_degrees

        self._motors = utils.motor.LimitedHeadedDefaultMotorGroup(
            motor_IDs,
            min_cumulative_encoder_counts=0,
            max_cumulative_encoder_counts=total_cumulative_encoder_counts,
        )

        self.set_speed(0)

    def set_speed(self, speed: float):
        self._motors.set_output(speed)

    def get_cumulative_encoder(self):
        return self._motors.get_cumulative_distance()

    def get_angle(self):
        return self._motors.get_percent_limit()

    def get_angular_velocity(self):
        return self._motors.get_lead_encoder_velocity() \
            * self._TOTAL_CUMULATIVE_ENCODER_COUNTS / self._ANGLE_RANGE
