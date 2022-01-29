import wpilib
import commands2

from robot_container import RobotContainer
import input

class Robot(commands2.TimedCommandRobot):
    def robotInit(self) -> None:
        self._container = RobotContainer()

        return super().robotInit()
    
    def robotPeriodic(self) -> None:
        commands2.CommandScheduler.getInstance().run()

        return super().robotPeriodic()
    
    def _simulationPeriodic(self) -> None:
        
        return super()._simulationPeriodic()

    def autonomousInit(self) -> None:
        self._auton_command = self._container.get_autonomous_command()
        if self._auton_command is not None:
            self._auton_command.schedule()
        
        return super().autonomousInit()
    
    def teleopInit(self) -> None:
        if getattr(self, '_auton_command', None) is not None:
            self._auton_command.cancel()

        return super().teleopInit()
    
    def teleopPeriodic(self) -> None:
        wpilib.SmartDashboard.putNumber('left speed', input.get_tank_left_speed())
        wpilib.SmartDashboard.putNumber('right speed', input.get_tank_right_speed())

        return super().teleopPeriodic()

if __name__ == '__main__':
    wpilib.run(Robot)