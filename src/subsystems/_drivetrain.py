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
        self._calculate_odometry()

        wpilib.SmartDashboard.putNumber('Dirvetrain Left Encoder', self.get_left_encoder_position())
        wpilib.SmartDashboard.putNumber('Dirvetrain Right Encoder', self.get_right_encoder_position())

        return super().periodic()

    def simulationPeriodic(self) -> None:
        self._left_sim_collection.setIntegratedSensorVelocity(self._intended_left_speed)
        self._right_sim_collection.setIntegratedSensorVelocity(self._intended_right_speed)

        return super().simulationPeriodic()

    def __init__(self) -> None:
        commands2.SubsystemBase.__init__(self)

        self._left_motors = utils.HeadedDefaultMotorGroup(constants.Drivetrain.LeftMotor.IDs)
        self._right_motors = utils.HeadedDefaultMotorGroup(constants.Drivetrain.RightMotor.IDs)
        self._right_motors.set_inverted()

        self.reset_encoders()

        self._gyro = navx.AHRS(wpilib.SPI.Port.kOnboardCS0)

        self.reset_gyro()

        self._simulation_init()

        self._init_odometry()

    def _simulation_init(self):
        self._intended_left_speed = 0
        self._intended_right_speed = 0

        self._left_sim_collection = self._left_motors.lead.getSimCollection()
        self._right_sim_collection = self._right_motors.lead.getSimCollection()

    def set_speed(self, left: float, right: float):
        """Sets the speed of the left and right motors."""
        self._intended_left_speed = left
        self._intended_right_speed = right

        self._left_motors.lead.set(ctre.ControlMode.PercentOutput, left)
        self._right_motors.lead.set(ctre.ControlMode.PercentOutput, right)

    def reset_encoders(self):
        """Zeroes the encoders and stored cumulative encoder values."""
        self._left_motors.reset_lead_encoder()
        self._right_motors.reset_lead_encoder()

        self._last_left_raw_encoder_ticks = 0
        self._last_right_raw_encoder_ticks = 0

    def get_left_encoder_position(self):
        """Returns the position of the drivetrain left encoder."""
        return self._left_motors.get_lead_encoder_position() or 0

    def get_left_encoder_speed(self):
        """Returns the speed of the drivetrain left encoder."""
        return self._left_motors.get_lead_encoder_velocity() or 0

    def get_right_encoder_position(self):
        """Returns the position of the drivetrain right encoder."""
        return self._right_motors.get_lead_encoder_position() or 0

    def get_right_encoder_speed(self):
        """Returns the speed of the drivetrain right encoder."""
        return self._right_motors.get_lead_encoder_velocity() or 0

    def get_wheel_speeds(self):
        return wpimath.kinematics.DifferentialDriveWheelSpeeds(
            self.get_left_encoder_speed(),
            self.get_right_encoder_speed(),
        )

    def get_gyro(self):
        return self._gyro.getRotation2d()

    def reset_gyro(self):
        self._gyro.reset()

    def get_rate(self):
        return self._gyro.getRate()

    def _init_odometry(self):
        self._odometry = wpimath.kinematics.DifferentialDriveOdometry(
            self._gyro.getRotation2d(),
        )

        self._left_cum_encoder_ticks = 0
        self._right_cum_encoder_ticks = 0

        self._last_left_raw_encoder_ticks = 0
        self._last_right_raw_encoder_ticks = 0

        self._left_encoder_delta = 0
        self._right_encoder_delta = 0

    def reset_odometry(self, pose: wpimath.geometry.Pose2d):
        self.reset_encoders()
        self._odometry.resetPosition(pose, self.get_gyro())

    def _update_odometry(self):
        self._calculate_odometry()

        self._odometry.update(
            self._gyro.getRotation2d(),
            self._get_last_left_distance(),
            self._get_last_right_distance(),
        )

    def _calculate_odometry(self):
        left_raw_encoder_ticks = self.get_left_encoder_position()
        right_raw_encoder_ticks = self.get_right_encoder_position()

        self._left_encoder_delta = left_raw_encoder_ticks - self._last_left_raw_encoder_ticks
        self._right_encoder_delta = right_raw_encoder_ticks - self._last_right_raw_encoder_ticks

        self._last_left_raw_encoder_ticks = left_raw_encoder_ticks
        self._last_right_raw_encoder_ticks = right_raw_encoder_ticks
        
        self._left_encoder_delta += ((self.get_left_encoder_speed > 0) + (self._left_encoder_delta < 0) - 1) * constants.Drivetrain.ENCODER_COUNTS_PER_ROTATION
        self._right_encoder_delta += ((self.get_right_encoder_speed > 0) + (self._right_encoder_delta < 0) - 1) * constants.Drivetrain.ENCODER_COUNTS_PER_ROTATION

        # Previous two lines are equivalent to:
        '''
        if self.get_left_encoder_speed() > 0:
            if left_encoder_delta < 0:
                left_encoder_delta += constants.Drivetrain.ENCODER_COUNTS_PER_ROTATION
        elif self.get_left_encoder_speed() < 0:
            if left_encoder_delta > 0:
                left_encoder_delta -= constants.Drivetrain.ENCODER_COUNTS_PER_ROTATION
        
        if self.get_right_encoder_speed() > 0:
            if right_encoder_delta < 0:
                right_encoder_delta += constants.Drivetrain.ENCODER_COUNTS_PER_ROTATION
        elif self.get_right_encoder_speed() < 0:
            if right_encoder_delta > 0:
                right_encoder_delta -= constants.Drivetrain.ENCODER_COUNTS_PER_ROTATION
        '''

        self._left_cum_encoder_ticks += self._left_encoder_delta
        self._right_cum_encoder_ticks += self._right_encoder_delta

    def _get_last_left_distance(self):
        return self._left_encoder_delta / constants.Drivetrain.ENCODER_COUNTS_PER_METER

    def _get_last_right_distance(self):
        return self._right_encoder_delta / constants.Drivetrain.ENCODER_COUNTS_PER_METER

    def get_pose(self):
        return self._odometry.getPose()