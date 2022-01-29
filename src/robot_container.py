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

        self._active_command_string_list = []

        def on_command_schedule(command: commands2.Command):
            self._active_command_string_list.append(command.getName())
            wpilib.SmartDashboard.putStringArray("Active Commands", self._active_command_string_list)
        
        def on_command_finish(command: commands2.Command):
            try:
                self._active_command_string_list.remove(command.getName())
            except ValueError:
                pass
            else:
                wpilib.SmartDashboard.putStringArray("Active Commands", self._active_command_string_list)
        
        commands2.CommandScheduler.getInstance().onCommandInitialize(on_command_schedule)
        commands2.CommandScheduler.getInstance().onCommandFinish(on_command_finish)
        commands2.CommandScheduler.getInstance().onCommandInterrupt(on_command_finish)

    def configure_bindings(self) -> None:
        input.get_intake \
            .whenPressed(commands.IntakeActivate()) \
            .whenReleased(commands.IntakeDeactivate())
    
    def get_autonomous_command(self) -> commands2.Command:
        ...
