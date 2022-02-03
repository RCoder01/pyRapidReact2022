import commands2

import subsystems


class TurretToAngle(commands2.CommandBase):

    def __init__(self):
        commands2.CommandBase.__init__(self)
        self.addRequirements(subsystems.turret)
