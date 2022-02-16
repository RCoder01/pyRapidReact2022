import warnings
import commands2
import commands2.button
import ctre
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
        # self.init_ball_counting()

        from commands.shooter.__shooter_power import ShooterPower
        _mo_command = ShooterPower(subsystems.shooter.mo, 'mo')
        _lester_command = ShooterPower(subsystems.shooter.lester, 'lester')
        subsystems.shooter.mo.setDefaultCommand(_mo_command)
        subsystems.shooter.lester.setDefaultCommand(_lester_command)
        def reset_molester():
            wpilib.SmartDashboard.putNumber("Shooter Power mo", 0)
            wpilib.SmartDashboard.putNumber("Shooter Power lester", 0)

        commands2.button.JoystickButton(wpilib.XboxController(0), wpilib.XboxController.Button.kX) \
            .whenPressed(reset_molester)
        
        # self._hood_motor = ctre.TalonFX(-1)
        # self._hood_motor.setNeutralMode(ctre.NeutralMode.Brake)

    def configure_bindings(self) -> None:
        # oi.Intake.activate \
        #     .whenPressed(commands.intake.SetActive()) \
        #     .whenReleased(commands.intake.SetInactive())

        # oi.Turret.manual_control \
        #     .whenHeld(commands.shooter.TurretManualControl(oi.Turret.turret_speed))

        # oi.exgest \
        #     .whenHeld(commands.Exgest())
        pass

    def configure_default_commands(self) -> None:
        # subsystems.drivetrain.setDefaultCommand(commands.drivetrain.ArcadeDrive(
        #     oi.Drivetrain.ArcadeDrive.get_forward_speed,
        #     oi.Drivetrain.ArcadeDrive.get_turn_speed,
        # ))
        # subsystems.feeder.setDefaultCommand(commands.feeder.Monitor())
        pass

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
