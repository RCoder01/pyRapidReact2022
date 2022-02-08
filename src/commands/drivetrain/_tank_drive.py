import commands2
import wpilib.drive

import subsystems


class TankDrive(commands2.CommandBase):
    def __init__(self, left_supplier, right_supplier) -> None:
        super().__init__(self)
        self.addRequirements(subsystems.drivetrain)
        self.setName('Tank Drive')

        self._left_supplier = left_supplier
        self._right_supplier = right_supplier

    def execute(self) -> None:
        subsystems.drivetrain.set_speed(self._left_supplier(), self._right_supplier())
        return super().execute()

    def isFinished(self) -> bool:
        return False

    def end(self, interrupted: bool) -> None:
        subsystems.drivetrain.set_speed(0, 0)
        return super().end(interrupted)
