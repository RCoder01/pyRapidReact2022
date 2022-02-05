import typing
import commands2

import utils


class Hood(commands2.SubsystemBase):
    def periodic(self):
        self._status = self._motors.periodic()

    def __init__(self, motor_IDs: typing.Collection[int], max_encoder_counts: int):
        commands2.SubsystemBase.__init__(self)

        self._motors = utils.LimitedHeadedDefaultMotorGroup(motor_IDs, max_cumulative_encoder_counts=max_encoder_counts)
        self._MAX_ENCODER_COUNTS = max_encoder_counts

    def set_speed(self, speed: float):
        if self._status is utils.LimitedHeadedDefaultMotorGroup.Status.WITHIN_BOUNDS:
            self._motors.set_speed(speed)
            return True
        return False

    def get_percent_extension(self):
        return self._motors.get_cumulative_distance() / self._MAX_ENCODER_COUNTS
