import wpilib
import wpilib.simulation
import commands2
import ctre

class Robot(commands2.TimedCommandRobot):
    def teleopInit(self) -> None:
    #     self.m = ctre.WPI_TalonFX(2)
    #     self.ms = [ctre.WPI_TalonFX(id) for id in (6, 7, 8)]
    #     map(lambda motor: motor.setNeutralMode(ctre.NeutralMode.Coast), self.ms)
        self.sensor = wpilib.DigitalInput(0)
        self.simsensor = wpilib.simulation.DIOSim(self.sensor)
        self.timer = wpilib.Timer()
    def teleopPeriodic(self) -> None:
        # wpilib.SmartDashboard.putNumber("encoder distance", self.m.getSelectedSensorPosition())
        wpilib.SmartDashboard.putNumber("sensor output", self.sensor.get())
        wpilib.SmartDashboard.putData("sensor", self.sensor)
        if self.timer.getFPGATimestamp() % 2 // 1:
            self.simsensor.setValue(True)
        else:
            self.simsensor.setValue(False)
        wpilib.SmartDashboard.putNumber('fpgatimestamp', self.timer.getFPGATimestamp() % 2 // 1)
        return super().teleopPeriodic()

if __name__ == '__main__':
    wpilib.run(Robot)
