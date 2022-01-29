import commands2
import ctre
import wpilib

import constants


class Intake(commands2.SubsystemBase):
    
    def periodic(self) -> None:
        wpilib.SmartDashboard.putNumber("Intake Speed", self.get_current_speed())

        super().periodic()
    
    def __init__(self) -> None:
        commands2.SubsystemBase.__init__(self)

        self._motors = [ctre.TalonFX(ID) for ID in constants.Intake.IDs]
        self._lead_motor = self._motors[0]
        for motor in self._motors[1:]:
            motor.follow(self._lead_motor)
    
    def set_speed(self, speed: float) -> None:
        """Sets the speed of the intake motors."""
        self._speed = speed
        self._lead_motor.set(ctre.ControlMode.PercentOutput, speed)
    
    def get_intended_speed(self) -> float:
        """Returns the set speed of the intake motor."""
        ...
    
    def get_current_speed(self) -> float:
        """Returns the actual speed of the intake motor."""
        ...