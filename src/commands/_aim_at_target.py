import commands2
import wpimath.controller

import constants
import subsystems


class AimAtTarget(commands2.CommandBase):
    """Control mode where the robot will rotate to face and maintain the target."""

    def __init__(self) -> None:
        super().addRequirements(subsystems.drivetrain)
        super().setName("AimAtTarget")

        self._controller = wpimath.controller.PIDController(
            constants.LimelightConstants.kP,
            constants.LimelightConstants.kI,
            constants.LimelightConstants.kD,
        )
        
        self._controller.setSetpoint(0)

    def execute(self) -> None:
        if subsystems.limelight.tv:
            output = self._controller.calculate(
                subsystems.limelight.tx
                * subsystems.limelight.ta
                * constants.LimelightConstants.Ka
            )

            subsystems.drivetrain.set_speed(output, -output)
        else:
            subsystems.drivetrain.set_speed(
                -constants.LimelightConstants.DEFAULT_ROTATION_SPEED,
                constants.LimelightConstants.DEFAULT_ROTATION_SPEED
            )

    def isFinished(self) -> bool:
        return self._controller.atSetpoint()

    def end(self) -> None:
        subsystems.drivetrain.set_speed(0, 0)