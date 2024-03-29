import warnings
import commands2
import commands2.button
import wpilib
import wpimath.filter
import wpimath.trajectory
import traceback

import commands

import constants
import oi
import subsystems


class RobotContainer():
    class CommandSchedulerEvent(RuntimeWarning):
        pass

    def __init__(self):
        self._configure_smartdashboard()
        self._configure_bindings()
        self._configure_default_commands()
        # self.init_ball_counting()

    def _configure_smartdashboard(self) -> None:
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

        def on_scheduler_event(event_type: str):
            def print_traceback(command: commands2.Command):
                print(f'Command "{command.getName()}" {event_type} with requirements {command.getRequirements()}')
                traceback.print_list(traceback.extract_stack()[6:-1])
            return print_traceback

        commands2.CommandScheduler.getInstance().onCommandInitialize(on_command_schedule)
        commands2.CommandScheduler.getInstance().onCommandFinish(on_command_finish)
        commands2.CommandScheduler.getInstance().onCommandInterrupt(on_command_finish)

        commands2.CommandScheduler.getInstance().onCommandInitialize(on_scheduler_event('initialized'))
        commands2.CommandScheduler.getInstance().onCommandFinish(on_scheduler_event('finished'))
        commands2.CommandScheduler.getInstance().onCommandInterrupt(on_scheduler_event('interrupted'))

    def _configure_bindings(self) -> None:
        # oi.Intake.activate \
        #     .whileHeld(commands.intake.Active())

        # oi.Feeder.manual_activate \
        #     .whileHeld(commands.belt.Active())

        # oi.Turret.manual_control \
        #     .whenHeld(commands.shooter.turret.ManualControl(oi.Turret.turret_speed))

        # oi.exgest \
        #     .whenHeld(commands.Exgest())

        # wpilib.SmartDashboard.putNumber("Mo Speed", 0)
        # oi.JoystickButton(oi._driver, oi._driver.Button.kLeftBumper) \
        #     .whenHeld(commands.shooter.josh.SetMoVariableSpeed(lambda: wpilib.SmartDashboard.getNumber("Mo Speed", 0)))

        # wpilib.SmartDashboard.putNumber("Lester Speed", 0)
        # oi.JoystickButton(oi._driver, oi._driver.Button.kRightBumper) \
        #     .whenHeld(commands.shooter.josh.SetLesterVariableSpeed(lambda: wpilib.SmartDashboard.getNumber("Lester Speed", 0)))

        # oi.JoystickButton(oi._driver, oi._driver.Button.kA) \
        #     .whenHeld(commands.shooter.feeder.Active())
        import wpimath.geometry
        import commands.shooter.turret._test_limelight
        # commands2.button.JoystickButton(oi._driver, oi._driver.Button.kB) \
        #     .whileHeld(commands.shooter.turret.ToHubAngle())
        commands2.button.JoystickButton(oi._driver, oi._driver.Button.kB) \
            .whileHeld(commands.shooter.turret._test_limelight.TargetHub())
        # commands2.button.JoystickButton(oi._driver, oi._driver.Button.kB) \
        #     .whileHeld(commands.shooter.turret.ToFieldAngle(wpimath.geometry.Rotation2d(-180)))
        commands2.button.JoystickButton(oi._driver, oi._driver.Button.kA) \
            .whenPressed(commands.shooter.turret.Callibrate().withTimeout(constants.Shooter.Turret.CALLIBRATION_TIMEOUT), False)
        commands2.button.JoystickButton(oi._driver, oi._driver.Button.kX) \
            .whenPressed(commands2.InstantCommand(lambda: subsystems.drivetrain.reset_odometry(wpimath.geometry.Pose2d(
                wpilib.SmartDashboard.getNumber('Drivetrain/Initial X', 0),
                wpilib.SmartDashboard.getNumber('Drivetrain/Initial Y', 0),
                wpilib.SmartDashboard.getNumber('Drivetrain/Initial Heading', 0),
            ))))
        # commands2.button.JoystickButton(oi._driver, oi._driver.Button.kX) \
        #     .whenPressed(commands2.PrintCommand('hi'))

        self.pd = wpilib.PowerDistribution()

    def _configure_default_commands(self) -> None:
        subsystems.drivetrain.setDefaultCommand(commands.drivetrain.ArcadeDrive(
            oi.Drivetrain.ArcadeDrive.get_forward_speed,
            oi.Drivetrain.ArcadeDrive.get_turn_speed,
        ))
        subsystems.belt.setDefaultCommand(commands.belt.Monitor())

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
            if (subsystems.belt.get_current_speed() > 0) ^ (not is_in):
                # If entering belt
                capacity = constants.Misc.BallCounting.MAX_CAPACITY
                if ball_count_num >= capacity:
                    warnings.warn(f"Belt capacity exceeded: Setting balls to {ball_count_num}, which is greater than {capacity = }", RuntimeWarning)
                add_ball_count(1)
            else:
                # If exiting belt
                if ball_count_num <= 0:
                    warnings.warn(f"Belt empty and decreasing: Keeping balls at 0", RuntimeWarning)
                else:
                    add_ball_count(-1)

        in_sensor_debouncer = wpimath.filter.Debouncer(constants.Misc.BallCounting.IN_DEBOUNCE_TIME)
        out_sensor_debouncer = wpimath.filter.Debouncer(constants.Misc.BallCounting.OUT_DEBOUNCE_TIME)
        # commands2.button.Button(lambda: in_sensor_debouncer.calculate(subsystems.belt.get_in_sensor())) \
        #     .whenPressed(passed_sensor(True))
        # commands2.button.Button(lambda: out_sensor_debouncer.calculate(subsystems.belt.get_out_sensor())) \
        #     .whenPressed(passed_sensor(False))
