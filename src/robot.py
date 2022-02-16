import wpilib
import commands2

from robot_container import RobotContainer

class Robot(commands2.TimedCommandRobot):
    def robotInit(self) -> None:
        self._container = RobotContainer()

        return super().robotInit()

    def robotPeriodic(self) -> None:
        commands2.CommandScheduler.getInstance().run()

        return super().robotPeriodic()

    def autonomousInit(self) -> None:
        self._auton_command = self._container.get_autonomous_command()
        if self._auton_command is not None:
            self._auton_command.schedule()

    def teleopInit(self) -> None:
        if getattr(self, '_auton_command', None) is not None:
            self._auton_command.cancel()

    def teleopPeriodic(self) -> None:
        # wpilib.SmartDashboard.putNumber('Shooter Power mo', wpilib.XboxController(0).getRightY())
        # wpilib.SmartDashboard.putNumber('Shooter Power lester', wpilib.XboxController(0).getRightX())
        pass

if __name__ == '__main__':
    wpilib.run(Robot)
