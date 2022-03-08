# TODO: Finish this
import typing

import commands2
import wpilib

import constants
import utils.motor


class Hood(commands2.SubsystemBase):
    def periodic(self) -> None:
        wpilib.SmartDashboard.putNumber('Hood/Extension', self.get_percent_extension())

    def __init__(self, motor_IDs: typing.Collection[int]):
        commands2.SubsystemBase.__init__(self)
        self.setName('Hood')
        self._motors = utils.motor.TalonFXGroup(motor_IDs)
        self._motors.lead.configAllSettings(constants.Shooter.Hood.MOTOR_CONFIG)

    def set_angle(self, angle: float):
        self._motors.set_configured_setpoint(angle)

    def get_percent_extension(self):
        return self._motors.get_lead_encoder_position()

    def activate(self):
        self._motors.set_neutral_mode_brake()

    def deactivate(self):
        self._motors.set_neutral_mode_coast()
        self._motors.set_output(0)
