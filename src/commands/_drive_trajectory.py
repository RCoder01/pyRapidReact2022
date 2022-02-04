import typing
import commands2
import wpimath.controller
import wpimath.geometry
import wpimath.kinematics
import wpimath.spline
import wpimath.trajectory
import wpimath.trajectory.constraint

import constants
import subsystems


class DriveTrajectory(commands2.RamseteCommand):
    @typing.overload
    def __init__(self, controlVectors: typing.List[wpimath.spline.Spline5.ControlVector], /) -> None:
        pass
    @typing.overload
    def __init__(self, initial: wpimath.spline.Spline3.ControlVector, interiorWaypoints: typing.List[wpimath.geometry.Translation2d], end: wpimath.spline.Spline3.ControlVector, /) -> None:
        pass
    @typing.overload
    def __init__(self, start: wpimath.geometry.Pose2d, interiorWaypoints: typing.List[wpimath.geometry.Translation2d], end: wpimath.geometry.Pose2d, /) -> None:
        pass
    @typing.overload
    def __init__(self, waypoints: typing.List[wpimath.geometry._geometry.Pose2d], /) -> None:
        pass

    def __init__(self, *args) -> None:
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
                    *constants.Drivetrain.Characterization.FeedForward
                ),
                drive_kinematics,
                constants.Misc.MAX_VOLTAGE,
            )
        )

        subsystems.drivetrain.reset_odometry()

        commands2.RamseteCommand.__init__(
            self,
            wpimath.trajectory.TrajectoryGenerator.generateTrajectory(
                *args,
                config=trajectory_config,
            ),
            subsystems.drivetrain.get_pose,
            wpimath.controller.RamseteController(
                *constants.Drivetrain.Characterization.Ramesete,
            ),
            wpimath.controller.SimpleMotorFeedforwardMeters(
                *constants.Drivetrain.Characterization.FeedForward,
            ),
            drive_kinematics,
            subsystems.drivetrain.get_wheel_speeds,
            wpimath.controller.PIDController(
                *constants.Drivetrain.LeftMotor.PID,
            ),
            wpimath.controller.PIDController(
                *constants.Drivetrain.RightMotor.PID,
            ),
            subsystems.drivetrain.set_speed,
            subsystems.drivetrain,
        )

        self.setName("DriveTrajectory")
        self.addRequirements(subsystems.drivetrain)
