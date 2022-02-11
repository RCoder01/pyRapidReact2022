import commands2
import wpimath.controller

import constants
import subsystems
import utils.math


class TurretToAngle(commands2.CommandBase):
    def __init__(self, angle_supplier) -> None:
        commands2.CommandBase.__init__()
        self.addRequirements(subsystems.shooter.turret)
        self.setName('Turret To Angle')

        self._angle_supplier = angle_supplier
        self._heading_feed_forward = utils.math.HeadingFeedForward(constants.Shooter.Turret.FeedForward.H)
        self._PID_controller = wpimath.controller.PIDController(*constants.Shooter.Turret.PID)

    def initialize(self) -> None:
        self._PID_controller.reset()