import typing
import commands2

import utils


class Josh(commands2.SubsystemBase):
    def __init__(self, motor_ids: typing.Collection[int]):
        commands2.SubsystemBase.__init__(self)

        self._motors = utils.HeadedDefaultMotorGroup(motor_ids)

    def get_speed(self):
        return self._motors.get_lead_encoder_velocity() or 0

    def set_speed(self, speed: float):
        self._motors.set_speed(speed)
