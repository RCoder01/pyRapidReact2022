import wpilib
import commands2
import commands2.button
import wpimath.geometry

class Robot(wpilib.TimedRobot):
    def robotInit(self) -> None:
        self.field = wpilib.Field2d()
        self.field.getObject('Initial Pose').setPose(wpimath.geometry.Pose2d())
        wpilib.SmartDashboard.putData('Field', self.field)
        commands2.button.JoystickButton(wpilib.Joystick(0), 1).whenPressed(
            commands2.PrintCommand(str(self.field.getObject('Initial Pose').getPose()))
        )
        return super().robotInit()
    
    def robotPeriodic(self) -> None:
        return super().robotPeriodic()

if __name__ == '__main__':
    wpilib.run(Robot)
