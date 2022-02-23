import wpilib
import commands2
import ctre

class Robot(commands2.TimedCommandRobot):
    def teleopInit(self) -> None:
        self.m = ctre.WPI_TalonFX(2)
        self.ms = [ctre.WPI_TalonFX(id) for id in (6, 7, 8)]
        map(lambda motor: motor.setNeutralMode(ctre.NeutralMode.Coast), self.ms)
    def teleopPeriodic(self) -> None:
        wpilib.SmartDashboard.putNumber("encoder distance", self.m.getSelectedSensorPosition())
        return super().teleopPeriodic()

if __name__ == '__main__':
    wpilib.run(Robot)
