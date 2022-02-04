import typing
import commands2
import wpilib

import utils


class Intake(commands2.SubsystemBase):

    def periodic(self) -> None:
        wpilib.SmartDashboard.putNumber('Intake Speed', self.get_current_speed())

        return super().periodic()
    
    # def simulationPeriodic(self) -> None:
    #     wpilib.SmartDashboard.putNumber('Intake Motor Output', self._speed)
    #     return super().simulationPeriodic()
    
    def __init__(self, motor_IDs: typing.Collection[int]) -> None:
        commands2.SubsystemBase.__init__(self)

        self._motors = utils.HeadedDefaultMotorGroup(motor_IDs)

        self._speed = 0

    def set_speed(self, speed: float) -> None:
        """Sets the speed of the intake motors."""
        self._speed = speed
        self._motors.set_speed(speed)

    def get_intended_speed(self) -> float:
        """Returns the set speed of the intake motor."""
        return self._speed

    def get_current_speed(self) -> float:
        """Returns the actual speed of the intake motor."""
        return self._motors.get_lead_encoder_velocity() or 0
