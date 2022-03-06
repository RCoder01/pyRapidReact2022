import wpilib
import commands2
import commands

import robot_container
import constants
import subsystems

class Robot(commands2.TimedCommandRobot):
    def robotInit(self) -> None:
        self._container = robot_container.RobotContainer()
        self.turret_callibration_command = commands.shooter.turret.Callibrate().withTimeout(constants.Shooter.Turret.CALLIBRATION_TIMEOUT)

        return super().robotInit()

    def robotPeriodic(self) -> None:
        commands2.CommandScheduler.getInstance().run()

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

if __name__ == '__main__':
    wpilib.run(Robot)
