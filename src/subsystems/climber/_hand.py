from turtle import forward
import typing

import commands2
import rev

import constants
import utils.constants
import utils.motor


class Hand(commands2.SubsystemBase):
    def periodic(self) -> None:
        if self.get_closed_limit:
            self._motors.lead.set(0)

    def __init__(self, motor_IDs: typing.Collection[int], PID: utils.constants.PIDConfiguration, soft_limit: int) -> None:
        commands2.SubsystemBase.__init__(self)
        self._motors = utils.motor.CANSparkMaxGroup(motor_IDs)
        self._motors.lead.restoreFactoryDefaults()
        self._motors.lead.enableSoftLimit(self._motors.lead.SoftLimitDirection.kForward, soft_limit)

    def set_setpoint(self, revolutions: int):
        self._motors.set_setpoint(revolutions)

    def get_closed_limit(self):
        return self._motors.lead.getReverseLimitSwitch(constants.Climber.Hand.LIMIT_SWITCH_TYPE)
