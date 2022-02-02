# TODO: Update for new shooting system
import commands2
import wpimath.controller

import constants
import subsystems


class AimAtTarget(commands2.CommandBase):
    """Control mode where the robot will rotate to face and maintain the target."""

    def __init__(self) -> None:
        commands2.CommandBase.__init__(self)
        self.addRequirements(subsystems.drivetrain)
        self.setName("AimAtTarget")

        self._controller = wpimath.controller.PIDController(
            *constants.Limelight.PID
        )
        
        self._controller.setSetpoint(0)

    def execute(self) -> None:
        if subsystems.limelight.tv:
            output = self._controller.calculate(
                subsystems.limelight.tx
                * subsystems.limelight.ta
                * constants.Limelight.Ka
            )

            subsystems.drivetrain.set_speed(output, -output)
        else:
            subsystems.drivetrain.set_speed(
                -constants.Limelight.DEFAULT_ROTATION_SPEED,
                constants.Limelight.DEFAULT_ROTATION_SPEED
            )

        super().execute(self)

    def isFinished(self) -> bool:
        return self._controller.atSetpoint()

    def end(self, interrupted) -> None:
        subsystems.drivetrain.set_speed(0, 0)

        super().end(self, interrupted)
