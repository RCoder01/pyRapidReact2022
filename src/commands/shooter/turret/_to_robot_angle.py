import math
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

        self._setpoint = angle

    def execute(self) -> None:
        _angle_setpoint = self._setpoint
        if not (-180 <= _angle_setpoint < 180):
            _angle_setpoint %= 360
        if _angle_setpoint > 180:
            _angle_setpoint -= 360
        subsystems.shooter.turret.set_setpoint(self._setpoint)
        wpilib.SmartDashboard.putNumber('Turret/Robot Angle Setpoint', self._setpoint)

    def end(self, interrupted: bool) -> None:
        wpilib.SmartDashboard.delete('Turret/Robot Angle Setpoint')
        subsystems.shooter.turret.set_speed(0)
        return super().end(interrupted)
