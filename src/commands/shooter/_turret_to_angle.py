import commands2

import constants
import subsystems
import utils.math


class TurretToAngle(commands2.CommandBase):
    def __init__(self) -> None:
        commands2.CommandBase.__init__()
        self.addRequirements(subsystems.shooter.turret)
        self.setName('TurretToAngle')

        self._heading_feed_forward = utils.math.HeadingFeedForward(constants.Shooter.Turret.FeedForward.H)
        


