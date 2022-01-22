import wpilib
import commands2

from robot_container import RobotContainer

class Robot(commands2.TimedCommandRobot):
    def robotInit(self) -> None:
        self._container = RobotContainer()
    
    def robotPeriodic(self) -> None:
        commands2.CommandScheduler.getInstance().run()
    
    def autonomousInit(self) -> None:
        self._auton_command = self._container.get_autonomous_command()
        if self._auton_command is not None:
            self._auton_command.schedule()
    
    def teleopInit(self) -> None:
        if self._auton_command is not None:
            self._auton_command.cancel()


if __name__ == '__main__':
    wpilib.run()