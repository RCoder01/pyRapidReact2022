import math
import typing

import commands2
import navx
import wpilib
import wpilib.simulation
import wpimath.geometry
import wpimath.system
import wpimath.system.plant
import wpimath.kinematics

import constants
import utils.motor


class Drivetrain(commands2.SubsystemBase):
    def periodic(self) -> None:
        current_pose = self._update_odometry()
        self.field.setRobotPose(current_pose)

        wpilib.SmartDashboard.putString('Drivetrain/Pose', str(current_pose))
        wpilib.SmartDashboard.putNumber('Drivetrain/Left Speed', self._left_motors.get_configured_lead_encoder_velocity())
        wpilib.SmartDashboard.putNumber('Drivetrain/Left Position', self._left_motors.get_configured_lead_encoder_position())
        wpilib.SmartDashboard.putNumber('Drivetrain/Right Speed', self._right_motors.get_configured_lead_encoder_velocity())
        wpilib.SmartDashboard.putNumber('Drivetrain/Right Position', self._right_motors.get_configured_lead_encoder_position())
        wpilib.SmartDashboard.putNumber('Drivetrain/Left Voltage', self._left_motors.get_output_voltage())
        wpilib.SmartDashboard.putNumber('Drivetrain/Right Voltage', self._right_motors.get_output_voltage())

        # wpilib.SmartDashboard.putNumber('Gyro Rot2D', self.get_gyro().degrees())
        # wpilib.SmartDashboard.putNumber('Gyro Angle', self._gyro.getAngle())
        # wpilib.SmartDashboard.putNumber('Left Motor Output Percent', self._left_motors.lead.getMotorOutputPercent() * 100)
        # wpilib.SmartDashboard.putNumber('Right Motor Output Percent', self._right_motors.lead.getMotorOutputPercent() * 100)

    def simulationPeriodic(self) -> None:
        self._drivetrain_sim.setInputs(
            self._left_motors.get_output_voltage(),
            self._right_motors.get_output_voltage(),
        )
        self._drivetrain_sim.update(constants.Misc.SIMULATION_PERIOD_MS / 1000)

        self._left_sim.set_configured_distance(self._drivetrain_sim.getLeftPosition())
        self._left_sim.set_configured_velocity(self._drivetrain_sim.getLeftVelocity())
        self._right_sim.set_configured_distance(-self._drivetrain_sim.getRightPosition())
        self._right_sim.set_configured_velocity(-self._drivetrain_sim.getRightVelocity())
        self._gyro.set_angle(self._drivetrain_sim.getHeading())

    def __init__(self) -> None:
        commands2.SubsystemBase.__init__(self)
        self.setName('Drivetrain')

        encoder_counts_per_meter = constants.Drivetrain.ENCODER_COUNTS_PER_METER
        self._left_motors = utils.motor.TalonFXGroup(constants.Drivetrain.LeftMotors.IDs)
        self._left_motors.configure_units(encoder_counts_per_meter)
        self._left_motors.set_neutral_mode_coast()
        self._right_motors = utils.motor.TalonFXGroup(constants.Drivetrain.RightMotors.IDs)
        self._right_motors.configure_units(encoder_counts_per_meter)
        self._right_motors.set_neutral_mode_coast()
        self._right_motors.invert_all()

        self.reset_encoders()

        self._gyro = navx.AHRS(wpilib.SPI.Port.kMXP)

        self.field = wpilib.Field2d()
        wpilib.SmartDashboard.putData('Field', self.field)

        self._init_odometry()

        self._simulation_init()

    def _simulation_init(self):
        characterization = constants.Drivetrain.Characterization
        self._drivetrain_sim = wpilib.simulation.DifferentialDrivetrainSim(
            wpimath.system.LinearSystemId.identifyDrivetrainSystem(
                characterization.LinearFeedForward.kV,
                characterization.LinearFeedForward.kA,
                characterization.AngularFeedForward.kV,
                characterization.AngularFeedForward.kA,
                characterization.TRACK_WIDTH,
            ),
            characterization.TRACK_WIDTH,
            wpimath.system.plant.DCMotor.falcon500(
                constants.Drivetrain.MOTORS_PER_SIDE
            ),
            constants.Drivetrain.GEAR_RATIO,
            constants.Drivetrain.WHEEL_RADIUS,
            # characterization.MEASUREMENT_STDDEVS,
        )

        class AHRSSim:
            def __init__(self) -> None:
                self._last_angle = wpimath.geometry.Rotation2d()
                self._angle = wpimath.geometry.Rotation2d()
            def set_angle(self, angle: wpimath.geometry.Rotation2d):
                self._last_angle = self._angle
                self._angle = angle
            def getRotation2d(self):
                return self._angle
            def getRate(self):
                -(self._angle - self._last_angle).degrees() * (1000 / constants.Misc.SIMULATION_PERIOD_MS)

        self._gyro = AHRSSim()

        self._left_sim = utils.motor.TalonFXGroupSim(self._left_motors)
        self._right_sim = utils.motor.TalonFXGroupSim(self._right_motors)


    def set_speed(self, left: float, right: float):
        """Sets the speed of the left and right motors."""
        self._intended_left_speed = left
        self._intended_right_speed = right

        self._left_motors.set_output(left)
        self._right_motors.set_output(right)

    def set_velocities(self, left: float, right: float):
        self._left_motors.set_configured_velocity(left)
        self._right_motors.set_configured_velocity(right)

    def reset_encoders(self):
        """Zeroes the encoders."""
        self._left_motors.reset_lead_encoder_position()
        self._right_motors.reset_lead_encoder_position()

    def get_left_encoder_position(self):
        """Returns the position of the drivetrain left encoder."""
        return self._left_motors.get_configured_lead_encoder_position()

    def get_left_encoder_speed(self):
        """Returns the speed of the drivetrain left encoder."""
        return self._left_motors.get_configured_lead_encoder_velocity()

    def get_right_encoder_position(self):
        """Returns the position of the drivetrain right encoder."""
        return self._right_motors.get_configured_lead_encoder_position()

    def get_right_encoder_speed(self):
        """Returns the speed of the drivetrain right encoder."""
        return self._right_motors.get_configured_lead_encoder_velocity()

    def get_wheel_speeds(self):
        """Returns the robot's speed in a wpilib DifferentialDriveWheelSpeeds object."""
        return wpimath.kinematics.DifferentialDriveWheelSpeeds(
            self.get_left_encoder_speed(),
            self.get_right_encoder_speed(),
        )

    def get_gyro(self):
        """Returns the gyro angle in a wpilib Rotation2d object."""
        return self._gyro.getRotation2d()

    def get_turn_rate(self):
        """Returns the robot's turn rate."""
        return self._gyro.getRate()

    def reset_odometry(self, pose: wpimath.geometry.Pose2d = wpimath.geometry.Pose2d()):
        """Resets the odometry to the given pose."""
        self.reset_encoders()
        self._odometry.resetPosition(pose, self.get_gyro())

    def _init_odometry(self):
        initial_x = wpilib.SmartDashboard.getNumber('Initial X', 0)
        initial_y = wpilib.SmartDashboard.getNumber('Initial Y', 0)
        initial_heading = wpilib.SmartDashboard.getNumber('Initial Heading', 0)

        self._odometry = wpimath.kinematics.DifferentialDriveOdometry(
            self.get_gyro(),
            wpimath.geometry.Pose2d(initial_x, initial_y, initial_heading),
        )

    def _update_odometry(self):
        """
        Updates the odometry object.

        Intended to be called periodically.
        """
        return self._odometry.update(
            self.get_gyro(),
            self.get_left_encoder_position(),
            self.get_right_encoder_position(),
        )

    def get_pose(self):
        """Returns the robot's pose in a wpilib Pose2d object."""
        return self._odometry.getPose()
