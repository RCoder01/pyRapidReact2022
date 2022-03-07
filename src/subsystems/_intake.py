import typing

import commands2
import wpilib

import constants
import utils.motor


class Intake(commands2.SubsystemBase):

    def periodic(self) -> None:
        wpilib.SmartDashboard.putNumber('Intake Speed', self.get_speed())

        return super().periodic()

    def __init__(self) -> None:
        commands2.SubsystemBase.__init__(self)
        self.setName('Intake')

        self._motors = utils.motor.TalonFXGroup(constants.Intake.MOTOR_IDs)

    def set_speed(self, speed: float) -> None:
        """Sets the speed of the intake motors."""
        self._speed = speed
        self._motors.set_output(speed)

    def get_speed(self) -> float:
        """Returns the actual speed of the intake motor."""
        return self._motors.get_lead_encoder_velocity()
