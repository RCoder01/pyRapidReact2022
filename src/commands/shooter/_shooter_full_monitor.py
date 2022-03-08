import commands2

import shooter_numbers
import subsystems

from . import hood
from . import josh


class ShooterFullMonitor(commands2.ParallelCommandGroup):
    def get_shooter_config(self):
        self.distance = subsystems.limelight.distance
        return shooter_numbers[
            min(
                shooter_numbers.positions_list,
                lambda distance: abs(distance - self.distance)
            )
        ]
    
    def get_mo(self):
        return self.get_shooter_config().mo
    def get_lester(self):
        return self.get_shooter_config().lester
    def get_hood(self):
        return self.get_shooter_config().hood

    def __init__(self):
        commands2.ParallelCommandGroup.__init__(
            self,
            [
                josh.SetLesterVariableSpeed
            ]
        )

        self.setName('Shooter Full Monitor')
        self.addRequirements(
            subsystems.shooter.hood,
            subsystems.shooter.mo,
            subsystems.shooter.lester
        )
