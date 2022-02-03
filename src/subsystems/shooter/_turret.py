import typing
import commands2
from wpilib import SmartDashboard

import utils
import constants


class Turret(commands2.SubsystemBase):

    def periodic(self) -> None:
        SmartDashboard.putNumber('Turret Encoder', self.get_encoder_value())

    def __init__(self, motor_IDs: typing.Collection[int]):
        commands2.SubsystemBase.__init__(self)

        self._motors = utils.HeadedDefaultMotorGroup(constants.Shooter.Turret.MOTOR_IDs)
    
    def set_speed(self, speed: float):
        self._motors.set_speed(speed)

    def get_encoder_value(self):
        self._motors.get_lead_encoder_position()
