import math
import commands2

import constants
import subsystems


class TargetHub(commands2.CommandBase):
    def __init__(self) -> None:
        commands2.CommandBase.__init__(self)
        self.setName('Turret Target Hub')
        self.addRequirements(subsystems.shooter.turret)
    
    def execute(self) -> None:
        if math.fabs(subsystems.limelight.tx) > constants.Limelight.X_TOLERANCE:
            subsystems.shooter.turret.set_speed(math.copysign(0.2, subsystems.limelight.tx))

    def end(self, interrupted: bool) -> None:
        subsystems.shooter.turret.set_speed(0)
        return super().end(interrupted)
