import math
import ctre
import wpilib

from utils.constants import (
    ConstantsClass,
    PIDConfiguration,
    PIDSetpointConfiguration,
    # ExtendedPIDConfiguration,
    FeedForwardConfiguration,
)



class Drivetrain(ConstantsClass):
    class LeftMotors(ConstantsClass):
        IDs = 1, 20
        PID = PIDConfiguration(Ki=0, Kd=0) # (https://docs.wpilib.org/en/stable/docs/software/pathplanning/trajectory-tutorial/creating-following-trajectory.html)

    class RightMotors(ConstantsClass):
        IDs = 2, 3
        PID = PIDConfiguration(Ki=0, Kd=0)

    ENCODER_COUNTS_PER_METER = 2048 * (7.82887701) / (0.15 * math.pi) # Encoder counts/revolution * gear ratio / (wheel diameter (meters) * pi = wheel circumference)

    class Characterization(ConstantsClass): # TODO: https://docs.wpilib.org/en/stable/docs/software/pathplanning/trajectory-tutorial/characterizing-drive.html

        FeedForward = FeedForwardConfiguration()

        TRACK_WIDTH = 0.88 # meters

        MAX_SPEED = 0 # meters per second
        MAX_ACCELERATION = 0 # meters per second per second

        class Ramesete(ConstantsClass):
            B = 2
            ZETA = 0.7

class Belt(ConstantsClass):
    MOTOR_IDs = 4,
    DEFAULT_SPEED = -0.5
    DEFAULT_EXGEST_SPEED = -DEFAULT_SPEED

    STAGING_RUN_TIME = 0.5

    IN_SENSOR_IDs = 0, 1
    OUT_SENSOR_IDs = 2, 3
    IN_SENSOR_DEBOUNCE_TIME = 0.5

class Intake(ConstantsClass):
    MOTOR_IDs = 8,
    DEFAULT_INTAKE_SPEED = 0.3
    DEFAULT_EXGEST_SPEED = -DEFAULT_INTAKE_SPEED

class Limelight(ConstantsClass):
    MOUNT_ANGLE = 0
    MOUNT_HEIGHT = 0
    TARGET_HEIGHT = 0

    Ka = 0
    PIPELINE = 1
    LED_MODE = 3
    X_TOLERANCE = 0.1

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

        CALLIBRATION_SPEED = -0.2
        CALLIBRATION_TIMEOUT = 5

        STANDARD_TOP_SPEED = 0.3

        PID = PIDConfiguration(0.1, 0.001)
        SETPOINT_TOLERANCE = 10
        FeedForward = FeedForwardConfiguration()
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
        MOTOR_CONFIG.forwardSoftLimitThreshold = 69000
        MOTOR_CONFIG.forwardSoftLimitThreshold = 69000
        MOTOR_CONFIG.reverseSoftLimitThreshold = 2000
        MOTOR_CONFIG.clearPositionOnLimitR = True

    class Hood(ConstantsClass):
        MOTOR_IDs = -6,
        EncoderLimits = (0, 2048)
        PID = PIDConfiguration()

    class Josh(ConstantsClass):
        class Mo(ConstantsClass):
            MOTOR_IDs = -7,
            SPEED_DECREASE_FACTOR = 1

            PID = PIDConfiguration(0.5)
            PIDTolerance = PIDSetpointConfiguration()
            FeedForward = FeedForwardConfiguration()

        class Lester(ConstantsClass):
            MOTOR_IDs = -8,
            SPEED_DECREASE_FACTOR = 1

            PID = PIDConfiguration(0.5)
            PIDTolerance = PIDSetpointConfiguration()
            FeedForward = FeedForwardConfiguration()


class Misc(ConstantsClass):
    SIMULATION_PERIOD_MS = 20
    MAX_VOLTAGE = 12

    ENCODER_COUNTS_PER_ROTATION = 2048

    MAX_VELOCITY_RPM = 5000

    class BallCounting(ConstantsClass):
        IN_DEBOUNCE_TIME = 0.1
        OUT_DEBOUNCE_TIME = 0.1

        MAX_CAPACITY = 2

    EXGEST_TIMEOUT = 5
