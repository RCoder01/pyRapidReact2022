import typing
import warnings

import commands2
from wpilib import SmartDashboard

import utils.motor
import utils.sensor
import utils.warnings


class Turret(commands2.SubsystemBase):

    def periodic(self) -> None:
        SmartDashboard.putNumber('Turret Percent', self.get_angle())

        self._motors.periodic()

        if self.get_limit_switch():
            self._motors.reset_odometry()

        # TODO: Sim stuff

    def __init__(self, motor_IDs: typing.Collection[int], sensor_IDs: typing.Collection[int], total_cumulative_encoder_counts: int, angle_range_degrees: float = 1):
        commands2.SubsystemBase.__init__(self)

        self._TOTAL_CUMULATIVE_ENCODER_COUNTS = total_cumulative_encoder_counts
        self._ANGLE_RANGE = angle_range_degrees

        self._motors = utils.motor.LimitedHeadedDefaultMotorGroup(
            motor_IDs,
            min_cumulative_encoder_counts=0,
            max_cumulative_encoder_counts=total_cumulative_encoder_counts,
        )
        self._limit_switch = utils.sensor.DoubleDigitialInput(*sensor_IDs, False, True)

        self.set_speed(0)

    def set_speed(self, speed: float):
        self._motors.set_output(speed)

    def get_cumulative_encoder(self):
        return self._motors.get_cumulative_distance()

    def get_angle(self):
        return self._motors.get_percent_limit() * self._ANGLE_RANGE

    def get_angular_velocity(self):
        return self._motors.get_lead_encoder_velocity() \
            * self._TOTAL_CUMULATIVE_ENCODER_COUNTS / self._ANGLE_RANGE

    def get_limit_switch(self):
        if self._limit_switch.get_error_state():
            warnings.warn('Turret limit switch disagreement', utils.warnings.LikelyHardwareError)
        return self._limit_switch.get_leniant()
