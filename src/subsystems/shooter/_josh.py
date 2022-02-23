import typing

import commands2

import utils.motor


class Josh(commands2.SubsystemBase):
    def periodic(self):
        ...

    def __init__(self, motor_ids: typing.Collection[int], gear_speed_increase: float):
        commands2.SubsystemBase.__init__(self)
        self.setName('Josh')

        self._motors = utils.motor.HeadedDefaultMotorGroup(motor_ids)
        self._motors.configure_units(gear_speed_increase)

        self.set_output(0)

    def get_jeff(self) -> float:
        return self._motors.get_lead_encoder_velocity() or 0

    def set_output(self, output: float):
        self._motors.set_output(output)

    def set_velocity_rpm(self, rpm: int):
        self._motors.set_configured_velocity(rpm / 60)

    def set_neutral_coast(self):
        self._motors.set_neutral_mode_coast()

    def set_neutral_brake(self):
        self._motors.set_neutral_mode_brake()
