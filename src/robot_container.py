import warnings
import commands2
import commands2.button
import wpilib
import wpimath.filter
import wpimath.trajectory

import commands
import constants
import oi
import subsystems


class RobotContainer():
    def __init__(self):
        active_command_string_list = []

        def on_command_schedule(command: commands2.Command):
            nonlocal active_command_string_list
            active_command_string_list.append(command.getName())
            wpilib.SmartDashboard.putStringArray("Active Commands", active_command_string_list)

        def on_command_finish(command: commands2.Command):
            nonlocal active_command_string_list
            try:
                active_command_string_list.remove(command.getName())
            except ValueError:
                pass
            else:
                wpilib.SmartDashboard.putStringArray("Active Commands", active_command_string_list)

        commands2.CommandScheduler.getInstance().onCommandInitialize(on_command_schedule)
        commands2.CommandScheduler.getInstance().onCommandFinish(on_command_finish)
        commands2.CommandScheduler.getInstance().onCommandInterrupt(on_command_finish)

        self.configure_bindings()
        self.configure_default_commands()
        self.init_ball_counting()

    def configure_bindings(self) -> None:
        oi.Intake.activate \
            .whenPressed(commands.intake.SetActive()) \
            .whenReleased(commands.intake.SetInactive())

        # oi.Turret.manual_control \
            # .whenHeld(commands.shooter.turret.ManualControl(oi.Turret.turret_speed))

        oi.exgest \
            .whenHeld(commands.Exgest())

        # self.pd = wpilib.PowerDistribution()

    def configure_default_commands(self) -> None:
        subsystems.drivetrain.setDefaultCommand(commands.drivetrain.ArcadeDrive(
            oi.Drivetrain.ArcadeDrive.get_forward_speed,
            oi.Drivetrain.ArcadeDrive.get_turn_speed,
        ))
        subsystems.feeder.setDefaultCommand(commands.feeder.Monitor())

    def get_autonomous_command(self) -> commands2.Command:
        trajectory_generator = wpimath.trajectory.TrajectoryGenerator.generateTrajectory(
            
        )
    
    def init_ball_counting(self) -> None:
        wpilib.SmartDashboard.putNumber("Stored Balls", 0)
        ball_count = wpilib.SmartDashboard.getEntry("Stored Balls")
        def add_ball_count(num: int):
            ball_count.setDouble(ball_count.getDouble(0) + num)

        def passed_sensor(is_in: bool):
            nonlocal ball_count
            ball_count_num = ball_count.getDouble(0)
            if (subsystems.feeder.get_avg_current_speed() > 0) ^ (not is_in):
                # If entering feeder
                capacity = constants.Misc.BallCounting.MAX_CAPACITY
                if ball_count_num >= capacity:
                    warnings.warn(f"Feeder capacity exceeded: Setting balls to {ball_count_num}, which is greater than {capacity = }", RuntimeWarning)
                add_ball_count(1)
            else:
                # If exiting feeder
                if ball_count_num <= 0:
                    warnings.warn(f"Feeder empty and decreasing: Keeping balls at 0", RuntimeWarning)
                else:
                    add_ball_count(-1)

        in_sensor_debouncer = wpimath.filter.Debouncer(constants.Misc.BallCounting.IN_DEBOUNCE_TIME)
        out_sensor_debouncer = wpimath.filter.Debouncer(constants.Misc.BallCounting.OUT_DEBOUNCE_TIME)
        commands2.button.Button(lambda: in_sensor_debouncer.calculate(subsystems.feeder.get_in_sensor())) \
            .whenPressed(passed_sensor(True))
        commands2.button.Button(lambda: out_sensor_debouncer.calculate(subsystems.feeder.get_out_sensor())) \
            .whenPressed(passed_sensor(False))
