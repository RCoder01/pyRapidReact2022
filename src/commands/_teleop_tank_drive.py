from typing import Callable

import commands2

import subsystems


class TeleopTankDrive(commands2.CommandBase):
    """Controls drivetrain with tank drive controls"""

    def __init__(self, left_power_supplier: Callable[[], float], right_power_supplier: Callable[[], float]) -> None:
        super().addRequirements([subsystems.drivetrain])
        super().setName("TeleopTankDrive")

        self._left_power_supplier = left_power_supplier
        self._right_power_supplier = right_power_supplier

        super().__init__()
    
    def execute(self) -> None:
        subsystems.drivetrain.set_speed(
            self._left_power_supplier(),
            self._right_power_supplier()
        )
        
        super().execute()
    
    def isFinished(self) -> bool:
        return False