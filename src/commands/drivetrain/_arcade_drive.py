import commands2
import wpilib.drive

import subsystems


class ArcadeDrive(commands2.CommandBase):
    def __init__(self, forward_supplier, turning_supplier) -> None:
        super().__init__(self)
        self.addRequirements(subsystems.drivetrain)
        self.setName('Arcade Drive')

        self._forward_supplier = forward_supplier
        self._turning_supplier = turning_supplier

    def execute(self) -> None:
        speeds = wpilib.drive.DifferentialDrive.arcadeDriveIK(self._forward_supplier(), self._turning_supplier(), False)

        subsystems.drivetrain.set_speed(speeds.left, speeds.right)
        return super().execute()

    def isFinished(self) -> bool:
        return False

    def end(self, interrupted: bool) -> None:
        subsystems.drivetrain.set_speed(0, 0)
        return super().end(interrupted)
