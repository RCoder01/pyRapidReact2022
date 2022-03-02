import commands2
import wpilib
import wpimath.controller

import constants
import subsystems


class ToRobotAngle(commands2.CommandBase):
    def __init__(self, angle: float) -> None:
        commands2.CommandBase.__init__(self)
        self.addRequirements(subsystems.shooter.turret)
        self.setName('Turret To Robot Angle')

        self._motor_feed_forward = wpimath.controller.SimpleMotorFeedforwardMeters(
            constants.Shooter.Turret.FeedForward.S,
            constants.Shooter.Turret.FeedForward.V,
            constants.Shooter.Turret.FeedForward.A,
        )

        self._PID_controller = wpimath.controller.PIDController(
            constants.Shooter.Turret.PID.P,
            constants.Shooter.Turret.PID.I,
            constants.Shooter.Turret.PID.D,
        )
        self._PID_controller.setTolerance(*constants.Shooter.Turret.PID.SetpointTolerance)

        self._setpoint = angle

    def initialize(self) -> None:
        self._PID_controller.setSetpoint(self._setpoint)
        self._motor_feed_forward.calculate(subsystems.shooter.turret.get_angular_velocity())

    def execute(self) -> None:
        wpilib.SmartDashboard.putNumber('Turret/Robot Angle Setpoint', self._setpoint)
        subsystems.shooter.turret.set_speed(self.calculate_output())

    def isFinished(self) -> bool:
        return self._PID_controller.atSetpoint()

    def end(self, interrupted: bool) -> None:
        wpilib.SmartDashboard.delete('Turret/Robot Angle Setpoint')
        subsystems.shooter.turret.set_speed(0)
        return super().end(interrupted)

    def calculate_output(self) -> float:
        output = 0
        output += self._PID_controller.calculate(subsystems.shooter.turret.get_angle(), self._setpoint)
        output += self._motor_feed_forward.calculate(subsystems.shooter.turret.get_angular_velocity())
