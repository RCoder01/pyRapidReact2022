import commands2

import constants
import subsystems


class Target(commands2.Command):

    def getRequirements(self) -> set[commands2.Subsystem]:
        return {subsystems.drivetrain}

    def execute(self) -> None:
        subsystems.drivetrain.set_speed(
            subsystems.limelight.tx * constants.TeleopConstants.TARGET_SPEED,
            -subsystems.limelight.tx * constants.TeleopConstants.TARGET_SPEED,
        )
    
    def isFinished(self) -> bool:
        return False
    
    def end(self) -> None:
        subsystems.drivetrain.set_speed(0, 0)