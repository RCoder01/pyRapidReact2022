import wpilib
import commands2
import ctre

class Robot(commands2.TimedCommandRobot):
    def robotPeriodic(self) -> None:
        commands2.CommandScheduler.getInstance().run()
        return super().robotPeriodic()
    def autonomousInit(self) -> None:
        m = [ctre.WPI_TalonFX(id) for id in (1, 2, 3, 4)]
        def execute():
            map(lambda motor: motor.setInverted(True), m[2:])
            map(lambda motor: motor.setVoltage(6), m)
        commands2.FunctionalCommand(lambda: None, execute, lambda interrupted: None, lambda: False).raceWith(commands2.WaitCommand(2))

if __name__ == '__main__':
    wpilib.run(Robot)
