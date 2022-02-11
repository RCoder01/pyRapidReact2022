import commands2
import wpilib.drive

import subsystems


class TankDrive(commands2.RunCommand):
    def __init__(self, left_supplier, right_supplier) -> None:
        run_function = lambda: subsystems.drivetrain.set_speed(left_supplier(), right_supplier())

        commands2.RunCommand.__init__(self, run_function)
        self.addRequirements(subsystems.drivetrain)
        self.setName('Tank Drive')

    def end(self, interrupted: bool) -> None:
        subsystems.drivetrain.set_speed(0, 0)
        return super().end(interrupted)
