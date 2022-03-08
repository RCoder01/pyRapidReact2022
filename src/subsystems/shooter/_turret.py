import enum
import math
import typing
import warnings

import commands2
import wpilib
import wpimath.geometry

import utils.motor
import utils.sensor
import utils.warnings
import constants


class Turret(commands2.SubsystemBase):
    class CallibrationStatus(enum.Enum):
        NEEDS_CALLIBRATION = 0
        CALLIBRATING = 1
        CALLIBRATED = 2

    @property
    def encoder_counts_per_degree(self):
        return self._encoder_counts_per_degree
    @encoder_counts_per_degree.setter
    def encoder_counts_per_degree(self, value):
        self._encoder_counts_per_degree = value

    def periodic(self) -> None:
        if self._motors.lead.hasResetOccurred():
            self.set_callibration_status(self.CallibrationStatus.NEEDS_CALLIBRATION)
        if self.get_callibration_status().value is self.CallibrationStatus.NEEDS_CALLIBRATION:
            self.config_max_speed(0)

        wpilib.SmartDashboard.putNumber('Turret/Callibration Status', self.get_callibration_status().value)
        wpilib.SmartDashboard.putNumber('Turret/Angular Velocity', self._motors.get_configured_lead_encoder_velocity())
        wpilib.SmartDashboard.putNumber('Turret/Robot Angle', self._motors.get_configured_lead_encoder_position())
        wpilib.SmartDashboard.putNumber('Turret/Raw Pos', self.get_raw_position())

        self.sim_collection.setLimitFwd(wpilib.SmartDashboard.getBoolean('Turret/Sim/Forward Limit Switch', False))
        self.sim_collection.setLimitRev(wpilib.SmartDashboard.getBoolean('Turret/Sim/Reverse Limit Switch', False))

    def __init__(self) -> None:
        commands2.SubsystemBase.__init__(self)
        self.setName('Turret')

        self._ANGLE_RANGE = constants.Shooter.Turret.ANGLE_MAX_DEGREES - constants.Shooter.Turret.ANGLE_MIN_DEGREES

        self._motors = utils.motor.TalonFXGroup(constants.Shooter.Turret.MOTOR_IDs)
        self._motors.configure_units(constants.Shooter.Turret.ENCODER_COUNTS_PER_DEGREE)
        self._motors.lead.configAllSettings(constants.Shooter.Turret.MOTOR_CONFIG)

        self.sim_collection = self._motors.lead.getSimCollection()
        wpilib.SmartDashboard.putBoolean('Turret/Sim/Forward Limit Switch', False)
        wpilib.SmartDashboard.putBoolean('Turret/Sim/Reverse Limit Switch', False)

        self.set_speed(0)
        self.set_callibration_status(self.CallibrationStatus.NEEDS_CALLIBRATION)

    def set_speed(self, speed: float):
        self._motors.set_output(speed)

    def set_setpoint(self, angle: float):
        self._motors.set_configured_setpoint(angle)

    def set_soft_offset(self, raw_offset: float):
        self._motors.set_soft_offset(raw_offset)

    def get_raw_position(self):
        return self._motors.get_lead_encoder_position()

    def get_angle(self):
        return self._motors.get_configured_lead_encoder_position()

    def get_angular_velocity(self):
        return self._motors.get_configured_lead_encoder_velocity()

    def get_robot_relative_rotation(self):
        return wpimath.geometry.Rotation2d(-self._motors.get_configured_lead_encoder_position())

    def get_forward_limit_switch(self):
        return self._motors.lead.isFwdLimitSwitchClosed()

    def get_reverse_limit_switch(self):
        return self._motors.lead.isRevLimitSwitchClosed()

    def config_max_speed(self, value: float = 1):
        value = max(min(math.fabs(value), 1), 0)
        wpilib.SmartDashboard.putNumber('Turret/Max Speed Config', value)
        self._motors.lead.configPeakOutputForward(value)
        self._motors.lead.configPeakOutputReverse(-value)

    def set_forward_soft_limit(self, value: bool):
        self._motors.lead.configForwardSoftLimitEnable(value)

    def set_reverse_soft_limit(self, value: bool):
        self._motors.lead.configReverseSoftLimitEnable(value)

    def set_callibration_status(self, status: CallibrationStatus):
        self._callibration_status = status

    def get_callibration_status(self):
        return self._callibration_status
