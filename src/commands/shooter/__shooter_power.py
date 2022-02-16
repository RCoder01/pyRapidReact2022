import commands2
from wpilib import SmartDashboard

import subsystems


class ShooterPower(commands2.CommandBase):
    def __init__(self, motor: subsystems.shooter._josh.Josh, name: str) -> None:
        commands2.CommandBase.__init__(self)
        self.addRequirements(motor)
        self._key = f'Shooter Power {name}'
        self.setName(self._key)

        self._motor = motor
        self._motor.set_neutral_coast()
        SmartDashboard.setDefaultNumber(self._key, 0)
        self._ignore_speed = False

    def execute(self):
        self._motor.set_output(SmartDashboard.getNumber(self._key, 0))

    def isFinished(self) -> bool:
        return False

    def end(self, interrupted: bool) -> None:
        self._motor.set_neutral_brake()
        self._motor.set_output(0)
        return super().end(interrupted)
