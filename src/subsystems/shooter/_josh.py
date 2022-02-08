import typing
import commands2
import ctre

import utils


class Josh(commands2.SubsystemBase):
    def periodic(self):
        ...

    def __init__(self, motor_ids: typing.Collection[int]):
        commands2.SubsystemBase.__init__(self)

        self._motors = utils.HeadedDefaultMotorGroup(motor_ids)

    def get_jeff(self):
        return self._motors.get_lead_encoder_velocity() or 0

    def set_output(self, output: float):
        self._motors.set_output(output)

    def set_neutral_coast(self):
        self._motors.set_netural_mode_coast()

    def set_neutral_brake(self):
        self._motors.set_netural_mode_brake()
