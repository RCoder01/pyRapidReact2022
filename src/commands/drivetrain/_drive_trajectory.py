import typing
import commands2
import wpilib
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

        left_PID_controller = wpimath.controller.PIDController(*constants.Drivetrain.LeftMotors.PID)
        right_PID_controller = wpimath.controller.PIDController(*constants.Drivetrain.RightMotors.PID)

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
            drive_kinematics,
            subsystems.drivetrain.set_velocities,
            subsystems.drivetrain,
        )

        self.setName("Drive Trajectory")
        self.addRequirements(subsystems.drivetrain)

        wpilib.SmartDashboard.putData("Left PID Controller", left_PID_controller)
        wpilib.SmartDashboard.putData("Right PID Controller", right_PID_controller)
