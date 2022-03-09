import math
import commands2
import wpilib
import wpimath.controller
import wpimath.geometry

import constants
import subsystems


class ToRobotAngle(commands2.CommandBase):
    def __init__(self, angle: wpimath.geometry.Rotation2d = wpimath.geometry.Rotation2d()) -> None:
        commands2.CommandBase.__init__(self)
        self.addRequirements(subsystems.shooter.turret)
        self.setName('Turret To Robot Angle')

        self._setpoint = self.optimize_setpoint(angle.degrees())

    def optimize_setpoint(self, angle: float) -> float:
        if not (-180 <= angle < 180):
            angle %= 360
        if angle > 180:
            angle -= 360
        return angle

    def execute(self) -> None:
        subsystems.shooter.turret.set_setpoint(self._setpoint)
        wpilib.SmartDashboard.putNumber('Turret/Robot Angle Setpoint', self._setpoint)

    def end(self, interrupted: bool) -> None:
        wpilib.SmartDashboard.delete('Turret/Robot Angle Setpoint')
        subsystems.shooter.turret.set_speed(0)
        return super().end(interrupted)
