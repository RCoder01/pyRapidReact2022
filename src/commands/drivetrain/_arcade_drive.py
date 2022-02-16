import typing
import commands2
from wpilib import SmartDashboard
import wpilib.drive

import subsystems

import utils.controls


class ArcadeDrive(commands2.CommandBase):
    def __init__(self, forward_supplier: typing.Callable[[], float], turning_supplier: typing.Callable[[], float]) -> None:
        commands2.CommandBase.__init__(self)
        self.addRequirements(subsystems.drivetrain)
        self.setName('Arcade Drive')

        self._forward_supplier = forward_supplier
        self._turning_supplier = turning_supplier

    def execute(self) -> None:
        speeds = wpilib.drive.DifferentialDrive.arcadeDriveIK(utils.controls.deadzone(self._forward_supplier()), utils.controls.deadzone(self._turning_supplier()), False)

        subsystems.drivetrain.set_speed(speeds.left, speeds.right)
        return super().execute()

    def isFinished(self) -> bool:
        return False

    def end(self, interrupted: bool) -> None:
        subsystems.drivetrain.set_speed(0, 0)
        return super().end(interrupted)
