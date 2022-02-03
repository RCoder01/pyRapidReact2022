import commands2

import utils
import constants


class Hood(commands2.SubsystemBase):
    def __init__(self):
        commands2.SubsystemBase.__init__(self)

        self._motors = utils.HeadedDefaultMotorGroup(constants.Shooter.Hood.MOTOR_IDs)

    def get_encoder_value(self):
        return self._motors.get_lead_encoder_position()