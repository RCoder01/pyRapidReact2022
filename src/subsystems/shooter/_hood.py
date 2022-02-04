import typing
import commands2

import utils


class Hood(commands2.SubsystemBase):
    def __init__(self, motor_IDs: typing.Collection[int]):
        commands2.SubsystemBase.__init__(self)

        self._motors = utils.HeadedDefaultMotorGroup(motor_IDs)

    def get_encoder_value(self):
        return self._motors.get_lead_encoder_position()
