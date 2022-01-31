from typing import Callable
import commands2

import subsystems


class TeleopShootSpeed(commands2.CommandBase):
    def __init__(self, shoot_speed_supplier: Callable[[], float]) -> None:
        commands2.CommandBase.__init__(self)

        self._shoot_speed_supplier = shoot_speed_supplier
    
    def execute(self) -> None:
        subsystems.shooter.set_jeff_setpoint(self._shoot_speed_supplier())

        return super().execute()
    
    def isFinished(self) -> bool:
        return False
    
    def end(self, interrupted: bool) -> None:
        subsystems.shooter.set_jeff_setpoint(0)
        return super().end(interrupted)
