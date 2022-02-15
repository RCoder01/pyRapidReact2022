import commands2
import wpimath.controller

import constants
import subsystems


class TurretToRobotAngle(commands2.CommandBase):
    def __init__(self, angle: float) -> None:
        commands2.CommandBase.__init__(self)
        self.addRequirements(subsystems.shooter.turret)
        self.setName('Turret To Robot Angle')

        ff_constants = constants.Shooter.Turret.FeedForward
        self._motor_feed_forward = wpimath.controller.SimpleMotorFeedforwardMeters(ff_constants.S, ff_constants.V, ff_constants.A)

        self._PID_controller = wpimath.controller.PIDController(*constants.Shooter.Turret.PID)
        self._PID_controller.setTolerance(*constants.Shooter.Turret.PID.SetpointTolerance)

        self._setpoint = angle

    def initialize(self) -> None:
        self._PID_controller.setSetpoint(self._setpoint)
        self._motor_feed_forward.calculate(subsystems.shooter.turret.get_angular_velocity())

    def execute(self) -> None:
        subsystems.shooter.turret.set_speed(self.calculate_output())

    def isFinished(self) -> bool:
        return self._PID_controller.atSetpoint()

    def end(self, interrupted: bool) -> None:
        subsystems.shooter.turret.set_speed(0)
        return super().end(interrupted)

    def calculate_output(self) -> float:
        output = 0
        output += self._PID_controller.calculate(subsystems.shooter.turret.get_angle(), self._setpoint)
        output += self._motor_feed_forward.calculate(subsystems.shooter.turret.get_angular_velocity())
