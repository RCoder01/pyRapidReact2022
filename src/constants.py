import math
import ctre

import wpimath.geometry

from utils.constants import (
    ConstantsClass,
    PIDConfiguration,
    PIDSetpointConfiguration,
    # ExtendedPIDConfiguration,
    FeedForwardConfiguration,
)



class Drivetrain(ConstantsClass):
    MOTORS_PER_SIDE = 2

    class LeftMotors(ConstantsClass):
        IDs = 1, 20
        PID = PIDConfiguration(Ki=0, Kd=0) # (https://docs.wpilib.org/en/stable/docs/software/pathplanning/trajectory-tutorial/creating-following-trajectory.html)

    class RightMotors(ConstantsClass):
        IDs = 2, 3
        PID = PIDConfiguration(Ki=0, Kd=0)

    GEAR_RATIO = 7.82887701
    WHEEL_RADIUS = 0.075

    ENCODER_COUNTS_PER_METER = 2048 * GEAR_RATIO / (WHEEL_RADIUS * 2 * math.pi) # Encoder counts/revolution * gear ratio / (wheel diameter (meters) * pi = wheel circumference)
    # ENCODER_COUNTS_PER_METER = 37600

    # 0.012 degrees gyro drift when standing still in 2 min 30 s

    class Characterization(ConstantsClass): # TODO: https://docs.wpilib.org/en/stable/docs/software/pathplanning/trajectory-tutorial/characterizing-drive.html

        LinearFeedForward = FeedForwardConfiguration(0.64434, 1.8175, 0.23827)
        AngularFeedForward = FeedForwardConfiguration(0.88663, 128.44, 15.542)

        TRACK_WIDTH = 0.88817 # meters
        # TRACK_WIDTH = 0.7493 # actual meters

        MAX_SPEED = 0 # meters per second
        MAX_ACCELERATION = 0 # meters per second per second

        class Ramesete(ConstantsClass):
            B = 2
            ZETA = 0.7

        # MEASUREMENT_STDDEVS = 0, 0, 0.0001, 0.1, 0.1, 0.005, 0.005

class Belt(ConstantsClass):
    MOTOR_IDs = 4,
    DEFAULT_SPEED = -0.5
    DEFAULT_EXGEST_SPEED = -DEFAULT_SPEED

    STAGING_RUN_TIME = 0.5
    TIMEOUT = 3

    IN_SENSOR_IDs = 0, 1
    OUT_SENSOR_IDs = 2, 3
    IN_SENSOR_DEBOUNCE_TIME = 0.5
    OUT_SENSOR_DEBOUNCE_TIME = 0.5

class Intake(ConstantsClass):
    MOTOR_IDs = 8,
    DEFAULT_INTAKE_SPEED = 0.3
    DEFAULT_EXGEST_SPEED = -DEFAULT_INTAKE_SPEED

class Limelight(ConstantsClass):
    MOUNT_ANGLE = 41.3 # degrees
    MOUNT_HEIGHT = 0.6477 # meters
    TARGET_HEIGHT = 2.6114375 # meters
    TARGET_RADIUS = 0.6096 # meters
    TURRET_MOUNT_POSITION = wpimath.geometry.Translation2d(0, 0)

    Ka = 0
    PIPELINE = 1
    LED_MODE = 3
    X_TOLERANCE = 1

class Shooter(ConstantsClass):
    class Feeder(ConstantsClass):
        MOTOR_IDs = 5,
        DEFAULT_SPEED = -0.5

    class Turret(ConstantsClass):
        MOTOR_IDs = 6,
        SENSOR_IDs = 4, 5
        SENSOR_INVERSIONS = True, True

        ENCODER_COUNTS_PER_DEGREE = 314
        ANGLE_MIN_DEGREES = -110
        ANGLE_MAX_DEGREES = 125.7
        CENTER = wpimath.geometry.Translation2d(0, 0)
        kL = 0.3

        CALLIBRATION_SPEED = -0.2
        CALLIBRATION_TIMEOUT = 5

        STANDARD_TOP_SPEED = 0.5

        PID = PIDConfiguration(0.1, 0.001)
        SETPOINT_TOLERANCE = 10
        FeedForward = FeedForwardConfiguration(kV = -0.3)
        HeadingFeedForward = 0

        MOTOR_CONFIG = ctre.TalonFXConfiguration()
        MOTOR_CONFIG.slot0 = ctre.SlotConfiguration()
        MOTOR_CONFIG.slot0.kP = 0.1
        MOTOR_CONFIG.slot0.kI = 0.001
        MOTOR_CONFIG.slot0.kD = 0
        MOTOR_CONFIG.slot0.kF = 0
        MOTOR_CONFIG.slot0.integralZone = 1000
        MOTOR_CONFIG.slot0.integralZone = 1000
        MOTOR_CONFIG.forwardSoftLimitEnable = True
        MOTOR_CONFIG.forwardSoftLimitThreshold = 65000
        MOTOR_CONFIG.reverseSoftLimitThreshold = 5000
        MOTOR_CONFIG.clearPositionOnLimitR = True

    class Hood(ConstantsClass):
        MOTOR_IDs = 9,
        EncoderLimits = (0, 2048)
        PID = PIDConfiguration()

        MOTOR_CONFIG = ctre.TalonFXConfiguration()
        MOTOR_CONFIG.slot0 = ctre.SlotConfiguration()
        
        MOTOR_CONFIG = ctre.TalonFXConfiguration()
        MOTOR_CONFIG.slot0 = ctre.SlotConfiguration()
        MOTOR_CONFIG.slot0.kP = 0.5
        MOTOR_CONFIG.slot0.kI = 0.01
        MOTOR_CONFIG.slot0.kD = 15
        MOTOR_CONFIG.slot0.kF = 0
        MOTOR_CONFIG.slot0.integralZone = 100
        MOTOR_CONFIG.neutralDeadband = 0
        

    class Josh(ConstantsClass):
        class Mo(ConstantsClass):
            MOTOR_IDs = 13,
            SPEED_INCREASE_FACTOR = 1

            MOTOR_CONFIG = ctre.TalonFXConfiguration()
            MOTOR_CONFIG.slot0 = ctre.SlotConfiguration()
            MOTOR_CONFIG.slot0.kP = 0.013
            MOTOR_CONFIG.slot0.kI = 0.0001
            MOTOR_CONFIG.slot0.kD = 0.01
            MOTOR_CONFIG.slot0.kF = 0.053
            MOTOR_CONFIG.slot0.maxIntegralAccumulator = 1e-8

        class Lester(ConstantsClass):
            MOTOR_IDs = 15,
            SPEED_INCREASE_FACTOR = 1

            MOTOR_CONFIG = ctre.TalonFXConfiguration()
            MOTOR_CONFIG.slot0 = ctre.SlotConfiguration()
            MOTOR_CONFIG.slot0.kP = 0.013
            MOTOR_CONFIG.slot0.kI = 5e-5
            MOTOR_CONFIG.slot0.kD = 0.01
            MOTOR_CONFIG.slot0.kF = 0.053
            MOTOR_CONFIG.slot0.maxIntegralAccumulator = 1e-8


class Misc(ConstantsClass):
    SIMULATION_PERIOD_MS = 20
    MAX_VOLTAGE = 12

    TALONFX_ENCODER_COUNTS_PER_ROTATION = 2048

    MAX_VELOCITY_RPM = 5000

    class BallCounting(ConstantsClass):
        IN_DEBOUNCE_TIME = 0.1
        OUT_DEBOUNCE_TIME = 0.1

        MAX_CAPACITY = 2

    EXGEST_TIMEOUT = 5
