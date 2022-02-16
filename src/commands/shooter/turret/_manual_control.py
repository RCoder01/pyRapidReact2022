import typing

import commands2

import utils.controls

import subsystems


class ManualControl(commands2.CommandBase):
    def __init__(self, power_supplier: typing.Callable[[], float]) -> None:
        commands2.CommandBase.__init__(self)
        self.setName('Turret Manual Control')
        self.addRequirements(subsystems.shooter.turret)

        self._power_supplier = power_supplier

    def initialize(self) -> None:
        subsystems.shooter.turret.set_speed(0)

    def execute(self) -> None:
        subsystems.shooter.turret.set_speed(utils.controls.deadzone(self._power_supplier()))

    def isFinished(self) -> bool:
        return False

    def end(self, interrupted: bool) -> None:
        subsystems.shooter.turret.set_speed(0)
        return super().end(interrupted)
