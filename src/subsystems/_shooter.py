import commands2
import wpilib

import constants


class Shooter(commands2.SubsystemBase):
    
    def periodic(self) -> None:
        wpilib.SmartDashboard.putNumber("Shooter Speed", self.get_speed())

        super().periodic()
    
    def __init__(self) -> None:
        self._motors = [MotorType(ID) for ID in constants.ShooterConstants.IDs]

        super().__init__()
    
    def set_speed_setpoint(self, speed: float) -> None:
        """Sets the speed of the shooter motors."""
        ...
    
    def get_speed_setpoint(self) -> float:
        """Returns the set speed of the shooter motor."""
        ...
    
    def get_speed(self) -> float:
        """Returns the actual speed of the shooter motor."""
        ...