import math
import typing

import commands2
import wpimath.controller
import wpimath.geometry

import utils.math

import constants
import subsystems


class TurretDefaultMode(commands2.CommandBase):
    def __init__(self) -> None:
        commands2.CommandBase.__init__()
        self.addRequirements(subsystems.shooter.turret)
        self.setName('Turret Default Mode')

        self._angle_supplier = lambda: subsystems.limelight.tx
        self._pose_supplier = subsystems.drivetrain.get_pose
        self._robot_angular_velocity_supplier = subsystems.drivetrain.get_turn_rate
        ff_constants = constants.Shooter.Turret.FeedForward
        self._motor_feed_forward = wpimath.controller.SimpleMotorFeedforwardMeters(ff_constants.S, ff_constants.V, ff_constants.A)
        self._heading_feed_forward = utils.math.HeadingFeedForward(ff_constants.H, self._pose_supplier())
        self._PID_controller = wpimath.controller.PIDController(*constants.Shooter.Turret.PID)
        self._setpoint = 0

    @property
    def _setpoint(self):
        # TODO: Calculate motion/distance-based setpoint
        return 0

    @_setpoint.setter
    def _setpoint(self, value: float):
        self._static_setpoint = value

    def initialize(self) -> None:
        self._PID_controller.reset()
        self._heading_feed_forward(self._pose_supplier())

    def execute(self) -> None:
        if subsystems.limelight.tv:
            hff = self._heading_feed_forward(self._pose_supplier())
            pid = self._PID_controller.calculate(self._angle_supplier(), self._setpoint + hff)
            mff = self._motor_feed_forward.calculate(subsystems.shooter.turret.get_angular_velocity())
            subsystems.shooter.turret.set_speed(pid + (mff / constants.Misc.MAX_VOLTAGE))
        else:
            # if self._robot_angular_velocity_supplier() > constants.Shooter.Turret.CRITICAL_ROBOT_ANGULAR_VELOCITY:
            #     self._setpoint = constants
            pass

    def isFinished(self) -> bool:
        return False

    def end(self, interrupted: bool) -> None:
        subsystems.shooter.turret.set_speed(0)
        return super().end(interrupted)

    @staticmethod
    def odometric_angle_to_hub():
        relative_to_hub = wpimath.geometry.Pose2d().relativeTo(subsystems.drivetrain.get_pose()).translation()
        return math.degrees(math.atan2(relative_to_hub.y, relative_to_hub.x))
