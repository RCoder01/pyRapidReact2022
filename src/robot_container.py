import commands2
import wpilib

import commands
import input
from subsystems import drivetrain


class RobotContainer():
    def __init__(self):
        self.configure_bindings()
        drivetrain.setDefaultCommand(commands.TeleopTankDrive(
            input.get_tank_left_speed,
            input.get_tank_right_speed,
        ))

    def configure_bindings(self) -> None:
    
    def get_autonomous_command(self) -> commands2.Command:
        ...