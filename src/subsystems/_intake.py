import commands2
import wpilib

import constants


class Intake(commands2.SubsystemBase):
    
    def periodic(self) -> None:
        wpilib.SmartDashboard.putNumber("Intake Speed", self.get_current_speed())

        super().periodic()
    
    def __init__(self) -> None:
        self._motors = [MotorType(ID) for ID in constants.IntakeConstants.IDs]
        
        super().__init__()
    
    def set_speed(self, speed: float) -> None:
        """Sets the speed of the intake motors."""
        ...
    
    def get_intended_speed(self) -> float:
        """Returns the set speed of the intake motor."""
        ...
    
    def get_current_speed(self) -> float:
        """Returns the actual speed of the intake motor."""
        ...