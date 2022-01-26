from typing import Callable

import commands2

import subsystems


class TeleopTankDrive(commands2.CommandBase):
    """Controls drivetrain with tank drive controls"""

    def __init__(self, left_power_supplier: Callable[[], float], right_power_supplier: Callable[[], float]) -> None:
        self.__init__()
        self.addRequirements(self, subsystems.drivetrain)
        self.setName(self, "TeleopTankDrive")

        self._left_power_supplier = left_power_supplier
        self._right_power_supplier = right_power_supplier
    
    def execute(self) -> None:
        subsystems.drivetrain.set_speed(
            self._left_power_supplier(),
            self._right_power_supplier()
        )
        
        self.execute()
    
    def isFinished(self) -> bool:
        return False