import math
import typing
import warnings

import commands2
import wpilib
import wpimath.geometry

import utils.motor
import utils.sensor
import utils.warnings


class Turret(commands2.SubsystemBase):
    @property
    def encoder_counts_per_degree(self):
        return self._encoder_counts_per_degree
    @encoder_counts_per_degree.setter
    def encoder_counts_per_degree(self, value):
        self._encoder_counts_per_degree = value

    def periodic(self) -> None:
        wpilib.SmartDashboard.putNumber('Turret\Angular Velocity', self._motors.get_configured_lead_encoder_velocity())
        wpilib.SmartDashboard.putNumber('Turret\Robot Angle', self._motors.get_configured_lead_encoder_position())
        wpilib.SmartDashboard.putBoolean('Turret\Clockwise Limit Switch', self.get_cw_limit_switch())
        wpilib.SmartDashboard.putBoolean('Turret\Counterclockwise Limit Switch', self.get_ccw_limit_switch())

    def __init__(
            self,
            motor_IDs: typing.Collection[int],
            sensor_IDs: tuple[int, int],
            sensor_inversions: tuple[int, int],
            angle_range_degrees: float = 360,
            encoder_counts_per_degree: int = 1,
            ) -> None:
        commands2.SubsystemBase.__init__(self)
        self.setName('Turret')

        self._ANGLE_RANGE = angle_range_degrees

        self._min_limit_switch = utils.sensor.SingleDigitalInput(sensor_IDs[0], sensor_inversions[0])
        self._max_limit_switch = utils.sensor.SingleDigitalInput(sensor_IDs[1], sensor_inversions[1])
        self.get_ccw_limit_switch = self._min_limit_switch.get
        self.get_cw_limit_switch = self._max_limit_switch.get

        self._motors = utils.motor.LimitedHeadedDefaultMotorGroup(
            motor_IDs,
            min_limit=lambda count: self._min_limit_switch.get(),
            max_limit=lambda count: self._max_limit_switch.get(),
        )
        self._motors.configure_units(encoder_counts_per_degree)

        self.set_speed(0)

    def set_speed(self, speed: float):
        self._motors.set_output(speed)

    def get_raw_position(self):
        return self._motors.get_lead_encoder_position()

    def get_angle(self):
        return self._motors.get_configured_lead_encoder_position

    def get_angular_velocity(self):
        return self._motors.get_configured_lead_encoder_velocity()

    def get_robot_relative_rotation(self):
        return wpimath.geometry.Rotation2d(-self._motors.get_configured_lead_encoder_position())
