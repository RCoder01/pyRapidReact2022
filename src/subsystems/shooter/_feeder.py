import typing

import commands2

import utils.motor


class Feeder(commands2.SubsystemBase):
    def __init__(self, motor_IDs: typing.Collection[float]) -> None:
        commands2.SubsystemBase.__init__(self)
        self.setName('Feeder')

        self._motor_group = utils.motor.HeadedDefaultMotorGroup(motor_IDs)

        self.set_speed(0)

    def set_speed(self, speed: float):
        """Set the speed of the feeder motors."""
        self._motor_group.set_output(speed)

    def get_current_speed(self):
        """Return the current speed of the feeder motors."""
        return self._motor_group.get_lead_encoder_velocity()
