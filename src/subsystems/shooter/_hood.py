# TODO: Finish this
import typing

import commands2

import utils.motor


class Hood(commands2.SubsystemBase):
    def __init__(self, motor_IDs: typing.Collection[int], /, min_encoder_counts: int, max_encoder_counts: int):
        commands2.SubsystemBase.__init__(self)
        self.setName('Hood')

        self._motors = utils.motor.LimitedHeadedDefaultMotorGroup(
            motor_IDs,
            min_encoder_counts=min_encoder_counts,
            max_encoder_counts=max_encoder_counts
        )

        self._status = utils.motor.LimitedHeadedDefaultMotorGroup.Status.WITHIN_BOUNDS
        self.set_speed(0)

    def set_speed(self, speed: float):
        if self._status is utils.motor.LimitedHeadedDefaultMotorGroup.Status.WITHIN_BOUNDS:
            self._motors.set_output(speed)
            return True
        return False

    def get_percent_extension(self):
        return self._motors.get_percent_limit()

    def activate(self):
        self._motors.set_neutral_mode_brake()

    def deactivate(self):
        self._motors.set_neutral_mode_coast()
        self._motors.set_output(0)
