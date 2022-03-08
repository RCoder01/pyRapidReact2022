import warnings
import wpilib
import commands2
import commands

import utils.commands
import utils.warnings
import robot_container
import constants
import subsystems

warnings.simplefilter('always', category=utils.warnings.SetpointOverrideWarning)

class Robot(commands2.TimedCommandRobot):
    def robotInit(self) -> None:
        self._container = robot_container.RobotContainer()
        self.turret_callibration_command = utils.commands.set_name(commands.shooter.turret.Callibrate().withTimeout(constants.Shooter.Turret.CALLIBRATION_TIMEOUT), "Turret Callibration w/ Timeout")

        return super().robotInit()

    def robotPeriodic(self) -> None:
        commands2.CommandScheduler.getInstance().run()

        # BIG TODO: Uncomment this
        if subsystems.shooter.turret.get_callibration_status() is subsystems.shooter.turret.CallibrationStatus.NEEDS_CALLIBRATION:
            self.turret_callibration_command.schedule(False)

        return super().robotPeriodic()

    def autonomousInit(self) -> None:
        self._autonomous_command = self._container.get_autonomous_command()
        if self._autonomous_command is not None:
            self._autonomous_command.schedule()

    def teleopInit(self) -> None:
        if getattr(self, '_auton_command', None) is not None:
            self._autonomous_command.cancel()

    def teleopPeriodic(self) -> None:
        pass

    def disabledInit(self) -> None:
        subsystems.shooter.hood.deactivate()

    def disabledExit(self) -> None:
        subsystems.shooter.hood.activate()

if __name__ == '__main__':
    wpilib.run(Robot)
