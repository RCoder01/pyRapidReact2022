import commands2

import constants


class Intake(commands2.Subsystem):
    
    def __init__(self) -> None:
        self._motors = [MotorType(ID) for ID in constants.IntakeConstants.IDs]
    
    def set_speed(self, speed: float) -> None:
        ...
    
    def getSensorValue(self) -> float:
        ...