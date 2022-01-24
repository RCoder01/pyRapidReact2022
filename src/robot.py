import wpilib
import commands2

from robot_container import RobotContainer

class Robot(commands2.TimedCommandRobot):
    def robotInit(self) -> None:
        self._container = RobotContainer()

        super().robotInit()
    
    def robotPeriodic(self) -> None:
        commands2.CommandScheduler.getInstance().run()

        super().robotPeriodic()
    
    def autonomousInit(self) -> None:
        self._auton_command = self._container.get_autonomous_command()
        if self._auton_command is not None:
            self._auton_command.schedule()
        
        super().autonomousInit()
    
    def teleopInit(self) -> None:
        if self._auton_command is not None:
            self._auton_command.cancel()

        super().teleopInit()


if __name__ == '__main__':
    wpilib.run(Robot)