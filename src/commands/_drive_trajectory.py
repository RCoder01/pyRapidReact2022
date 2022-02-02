import typing
import commands2
import wpilib
import wpimath.geometry
import wpimath.controller
import wpimath.kinematics
import wpimath.trajectory
import wpimath.trajectory.constraint

import constants
import subsystems


class DriveTrajectory(commands2.RamseteCommand):
    def __init__(self, waypoints: typing.Collection[wpimath.geometry.Pose2d]) -> None:
        drive_kinematics = wpimath.kinematics.DifferentialDriveKinematics(
            constants.Drivetrain.Characterization.TRACK_WIDTH,
        )

        trajectory_config = wpimath.trajectory.TrajectoryConfig(
            constants.Drivetrain.Characterization.MAX_SPEED,
            constants.Drivetrain.Characterization.MAX_ACCELERATION,
        )
        trajectory_config.setKinematics(drive_kinematics)
        trajectory_config.addConstraint(
            wpimath.trajectory.constraint.DifferentialDriveVoltageConstraint(
                wpimath.controller.SimpleMotorFeedforwardMeters(
                    constants.Drivetrain.Characterization.FeedForward.S,
                    constants.Drivetrain.Characterization.FeedForward.V,
                    constants.Drivetrain.Characterization.FeedForward.A,
                ),
                drive_kinematics,
                constants.Misc.MAX_VOLTAGE,
            )
        )

        subsystems.drivetrain.reset_odometry()

        super().__init__(
            wpimath.trajectory.TrajectoryGenerator.generateTrajectory(
                [], # TODO: Add waypoints
                config=trajectory_config,
            ),
            subsystems.drivetrain.get_pose,
            wpimath.controller.RamseteController(
                constants.Drivetrain.Characterization.Ramesete.B,
                constants.Drivetrain.Characterization.Ramesete.ZETA,
            ),
            wpimath.controller.SimpleMotorFeedforwardMeters(
                constants.Drivetrain.Characterization.FeedForward.S,
                constants.Drivetrain.Characterization.FeedForward.V,
                constants.Drivetrain.Characterization.FeedForward.A,
            ),
            drive_kinematics,
            subsystems.drivetrain.get_wheel_speeds,
            wpimath.controller.PIDController(
                constants.Drivetrain.LeftMotor.PID.P,
                constants.Drivetrain.LeftMotor.PID.I,
                constants.Drivetrain.LeftMotor.PID.D,
            ),
            wpimath.controller.PIDController(
                constants.Drivetrain.RightMotor.PID.P,
                constants.Drivetrain.RightMotor.PID.I,
                constants.Drivetrain.RightMotor.PID.D,
            ),
            subsystems.drivetrain.set_speed,
            subsystems.drivetrain,
        )