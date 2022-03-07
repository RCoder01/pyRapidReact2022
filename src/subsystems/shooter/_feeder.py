import typing

import commands2
import wpilib

import utils.motor
import constants


class Feeder(commands2.SubsystemBase):
    def periodic(self) -> None:
        wpilib.SmartDashboard.putNumber('Feeder Speed', self.get_speed())

    def __init__(self) -> None:
        commands2.SubsystemBase.__init__(self)
        self.setName('Feeder')

        self._motor_group = utils.motor.HeadedDefaultMotorGroup(constants.Shooter.Feeder.MOTOR_IDs)

        self.set_speed(0)

    def set_speed(self, speed: float):
        """Set the speed of the feeder motors."""
        self._motor_group.set_output(speed)

    def get_speed(self):
        """Return the current speed of the feeder motors."""
        return self._motor_group.get_lead_encoder_velocity()
