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
        this_left_encoder_position = self.get_left_encoder_position()
        this_right_encoder_position = self.get_right_encoder_position()

        self._left_distance = (this_left_encoder_position - self._last_left_encoder_position) / constants.Drivetrain.ENCODER_COUNTS_PER_METER
        self._right_distance = (this_right_encoder_position - self._last_right_encoder_position) / constants.Drivetrain.ENCODER_COUNTS_PER_METER

        self._last_left_encoder_position = this_left_encoder_position
        self._last_right_encoder_position = this_right_encoder_position

        self._odometry.update(
            self._gyro.getRotation2d(),
            self._left_distance,
            self._right_distance,
        )

        wpilib.SmartDashboard.putNumber('Dirvetrain Left Encoder', self.get_left_encoder_position())
        wpilib.SmartDashboard.putNumber('Dirvetrain Right Encoder', self.get_right_encoder_position())

        return super().periodic()
    
    def simulationPeriodic(self) -> None:
        self._left_sim_collection.setIntegratedSensorVelocity(self._left_speed)
        self._right_sim_collection.setIntegratedSensorVelocity(self._right_speed)

        return super().simulationPeriodic()

    def __init__(self) -> None:
        commands2.SubsystemBase.__init__(self)

        self._left_motors = utils.HeadedDefaultMotorGroup(constants.Drivetrain.LeftMotor.IDs)
        self._right_motors = utils.HeadedDefaultMotorGroup(constants.Drivetrain.RightMotor.IDs)
        self._right_motors.set_inverted()

        self._left_speed = 0
        self._right_speed = 0

        self.reset_encoders()

        self._last_left_encoder_position = self.get_left_encoder_position()
        self._last_right_encoder_position = self.get_right_encoder_position()

        self._gyro = navx.AHRS(wpilib.SPI.Port.kOnboardCS0)

        self.reset_gyro()

        self._odometry = wpimath.kinematics.DifferentialDriveOdometry(
            self._gyro.getRotation2d(),
        )

        self._left_sim_collection = self._left_motors.lead.getSimCollection()
        self._right_sim_collection = self._right_motors.lead.getSimCollection()
    
    def set_speed(self, left: float, right: float):
        """Sets the speed of the left and right motors."""
        self._left_speed = left
        self._right_speed = right

        self._left_motors.lead.set(ctre.ControlMode.PercentOutput, left)
        self._right_motors.lead.set(ctre.ControlMode.PercentOutput, right)

    def reset_encoders(self):
        """Zeroes the encoders."""
        self._left_motors.reset_lead_encoder()
        self._right_motors.reset_lead_encoder()

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

    def get_gyro(self):
        return self._gyro.getRotation2d()

    def reset_gyro(self):
        self._gyro.reset()

    def get_rate(self):
        return self._gyro.getRate()

    def get_wheel_speeds(self):
        return wpimath.kinematics.DifferentialDriveWheelSpeeds(
            self.get_left_encoder_speed(),
            self.get_right_encoder_speed(),
        )