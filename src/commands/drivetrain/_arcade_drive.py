import commands2
import wpilib.drive

import subsystems


class ArcadeDrive(commands2.RunCommand):
    def __init__(self, forward_supplier, turning_supplier) -> None:
        set_speeds = lambda speeds: subsystems.drivetrain.set_speed(speeds.left, speeds.right)
        run_function = lambda: set_speeds(wpilib.drive.DifferentialDrive.arcadeDriveIK(forward_supplier(), turning_supplier(), False))

        commands2.RunCommand.__init__(self, run_function)
        self.addRequirements(subsystems.drivetrain)
        self.setName('Arcade Drive')

    def end(self, interrupted: bool) -> None:
        subsystems.drivetrain.set_speed(0, 0)
        return super().end(interrupted)
