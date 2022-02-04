import typing
import commands2
import ctre
import navx
import wpilib
import wpilib.simulation
import wpimath.geometry
import wpimath.kinematics

import constants
import utils


class Drivetrain(commands2.SubsystemBase):

    def periodic(self) -> None:
        self._update_odometry()

        wpilib.SmartDashboard.putNumber('Drivetrain Left Encoder', self.get_left_encoder_position())
        wpilib.SmartDashboard.putNumber('Drivetrain Right Encoder', self.get_right_encoder_position())
        wpilib.SmartDashboard.putString('Drivetrain Pose', str(self.get_pose()))

        return super().periodic()

    def simulationPeriodic(self) -> None:
        self._left_sim_collection.setIntegratedSensorVelocity(self._intended_left_speed)
        self._right_sim_collection.setIntegratedSensorVelocity(self._intended_right_speed)

        return super().simulationPeriodic()

    def __init__(
            self,
            left_motor_IDs: typing.Collection[int],
            right_motor_IDs: typing.Collection[int],
            gyro_port: wpilib.SPI.Port,
            left_encoder_counts_per_meter: float,
            right_encoder_counts_per_meter: float = None
            ) -> None:
        commands2.SubsystemBase.__init__(self)

        self._left_motors = utils.OdometricHeadedDefaultMotorGroup(left_motor_IDs, left_encoder_counts_per_meter)
        self._right_motors = utils.OdometricHeadedDefaultMotorGroup(right_motor_IDs, right_encoder_counts_per_meter or left_encoder_counts_per_meter)
        # self._right_motors.set_inverted() # TODO

        self.reset_encoders()

        self._gyro = navx.AHRS(gyro_port)

        # TODO: Give this 1 sec delay or something
        self.reset_gyro()

        self._simulation_init()

        self._odometry = wpimath.kinematics.DifferentialDriveOdometry(
            self._gyro.getRotation2d(),
        )

    def _simulation_init(self):
        self._intended_left_speed = 0
        self._intended_right_speed = 0

        self._left_sim_collection = self._left_motors.lead.getSimCollection()
        self._right_sim_collection = self._right_motors.lead.getSimCollection()

    def set_speed(self, left: float, right: float):
        """Sets the speed of the left and right motors."""
        self._intended_left_speed = left
        self._intended_right_speed = right

        self._left_motors.set_speed(left)
        self._right_motors.set_speed(right)

    def reset_encoders(self):
        """Zeroes the encoders."""
        self._left_motors.reset_lead_encoder()
        self._right_motors.reset_lead_encoder()

    def get_left_encoder_position(self):
        """Returns the position of the drivetrain left encoder."""
        return self._left_motors.get_lead_encoder_position()

    def get_left_encoder_speed(self):
        """Returns the speed of the drivetrain left encoder."""
        return self._left_motors.get_lead_encoder_velocity()

    def get_right_encoder_position(self):
        """Returns the position of the drivetrain right encoder."""
        return self._right_motors.get_lead_encoder_position()

    def get_right_encoder_speed(self):
        """Returns the speed of the drivetrain right encoder."""
        return self._right_motors.get_lead_encoder_velocity()

    def get_wheel_speeds(self):
        """Returns the robot's speed in a wpilib DifferentialDriveWheelSpeeds object."""
        return wpimath.kinematics.DifferentialDriveWheelSpeeds(
            self.get_left_encoder_speed(),
            self.get_right_encoder_speed(),
        )

    def get_gyro(self):
        """Returns the gyro angle in a wpilib Rotation2d object."""
        return self._gyro.getRotation2d()

    def reset_gyro(self):
        """Resets the gyro heading to zero."""
        self._gyro.reset()

    def get_turn_rate(self):
        """Returns the robot's turn rate."""
        return self._gyro.getRate()

    def reset_odometry(self, pose: wpimath.geometry.Pose2d = None):
        """Resets the odometry to the given pose."""
        self._left_motors.reset_odometry()
        self._right_motors.reset_odometry()

        pose = pose or wpimath.geometry.Pose2d()
        self._odometry.resetPosition(pose, self.get_gyro())

    def _update_odometry(self):
        """
        Updates the odometry object.

        Intended to be called periodically.
        """
        self._left_motors.periodic()
        self._right_motors.periodic()

        self._odometry.update(
            self._gyro.getRotation2d(),
            self._get_last_left_distance(),
            self._get_last_right_distance(),
        )

    def _get_last_left_distance(self):
        """Returns the distance traveled by the left encoder in the last period."""
        return self._left_motors.get_last_distance()

    def _get_last_right_distance(self):
        """Returns the distance traveled by the right encoder in the last period."""
        return self._right_motors.get_last_distance()

    def get_pose(self):
        """Returns the robot's pose in a wpilib Pose2d object."""
        return self._odometry.getPose()
