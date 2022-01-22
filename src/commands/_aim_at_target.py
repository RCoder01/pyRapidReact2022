import commands2
import wpimath.controller

import constants
import subsystems


class AimAtTarget(commands2.Command):

    def getRequirements(self) -> set[commands2.Subsystem]:
        return {subsystems.drivetrain}
    
    def __init__(self) -> None:
        self._controller = wpimath.controller.PIDController(
            constants.LimelightConstants.kP,
            constants.LimelightConstants.kI,
            constants.LimelightConstants.kD,
        )
        
        self._controller.set_setpoint(0)

    def execute(self) -> None:
        output = self._controller.calculate(
            subsystems.limelight.tx
            * subsystems.limelight.ta
            * constants.LimelightConstants.Ka
        )

        subsystems.drivetrain.set_speed(output, -output)

    def isFinished(self) -> bool:
        return not subsystems.limelight.tv or self._controller.atSetpoint()
    
    def end(self) -> None:
        subsystems.drivetrain.set_speed(0, 0)