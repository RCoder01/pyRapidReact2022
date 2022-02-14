import commands2
import commands2.button
import wpilib
import wpimath.trajectory

import commands
import constants
import oi
import subsystems


class RobotContainer():
    def __init__(self):
        self.configure_bindings()
        self.configure_default_commands()

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
        oi.Intake.activate \
            .whenPressed(commands.intake.SetActive()) \
            .whenReleased(commands.intake.SetInactive())

        oi.Turret.manual_control \
            .whenHeld(commands.shooter.TurretManualControl())

        # oi. \
        #     .whenHeld(commands.feeder.SetActive(
        #         -constants.Feeder.TopMotors.DEFAULT_SPEED,
        #         -constants.Feeder.BottomMotors.DEFAULT_SPEED
        #     ))

    def configure_default_commands(self) -> None:
        subsystems.drivetrain.setDefaultCommand(commands.drivetrain.ArcadeDrive(
            oi.Drivetrain.ArcadeDrive.get_forward_speed,
            oi.Drivetrain.ArcadeDrive.get_turn_speed,
        ))
        subsystems.feeder.setDefaultCommand(commands.feeder.Monitor())

    def get_autonomous_command(self) -> commands2.Command:
        trajectory_generator = wpimath.trajectory.TrajectoryGenerator.generateTrajectory(
            
        )
