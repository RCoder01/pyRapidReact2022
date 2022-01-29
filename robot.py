import wpilib
import commands2

class ExampleSubsystem(commands2.SubsystemBase):
    ...

example_subsystem_instance = ExampleSubsystem()

class DefaultCommand(commands2.CommandBase):
    def __init__(self):
        commands2.CommandBase.__init__(self)
        self.addRequirements(example_subsystem_instance) # line 11
    
    def isFinished(self):
        return False

class Robot(commands2.TimedCommandRobot):
    def robotInit(self) -> None:
        example_subsystem_instance.setDefaultCommand(DefaultCommand()) # line 19

        return super().robotInit()

if __name__ == '__main__':
    wpilib.run(Robot) # line 24