import math
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
        IDs = 2, 6
        PID = PIDConfiguration(Ki=0, Kd=0) # (https://docs.wpilib.org/en/stable/docs/software/pathplanning/trajectory-tutorial/creating-following-trajectory.html)

    class RightMotors(ConstantsClass):
        IDs = 7, 8
        PID = PIDConfiguration(Ki=0, Kd=0)

    ENCODER_COUNTS_PER_METER = 2048 * (7.82887701) / (0.15 * math.pi) # Encoder counts/revolution * gear ratio / (wheel diameter (meters) * pi = wheel circumference)

    class Characterization(ConstantsClass): # TODO: https://docs.wpilib.org/en/stable/docs/software/pathplanning/trajectory-tutorial/characterizing-drive.html

        FeedForward = FeedForwardConfiguration()

        TRACK_WIDTH = 0.30 # meters

        MAX_SPEED = 0 # meters per second
        MAX_ACCELERATION = 0 # meters per second per second

        class Ramesete(ConstantsClass):
            B = 2
            ZETA = 0.7

class Belt(ConstantsClass):
    MOTOR_IDs = -2,
    DEFAULT_SPEED = -0.5
    DEFAULT_EXGEST_SPEED = -DEFAULT_SPEED

    STAGING_RUN_TIME = 0.5

    IN_SENSOR_IDs = 0, 1
    OUT_SENSOR_IDs = 2, 3
    IN_SENSOR_DEBOUNCE_TIME = 0.5

class Intake(ConstantsClass):
    MOTOR_IDs = -3,
    DEFAULT_INTAKE_SPEED = 0.3
    DEFAULT_EXGEST_SPEED = -DEFAULT_INTAKE_SPEED

class Limelight(ConstantsClass):
    MOUNT_ANGLE = 0

    Ka = 0
    PIPELINE = 1
    LED_MODE = 3
    X_TOLERANCE = 0.1

class Shooter(ConstantsClass):
    class Feeder(ConstantsClass):
        MOTOR_IDs = -4,
        DEFAULT_SPEED = -0.5

    class Turret(ConstantsClass):
        MOTOR_IDs = -5,
        SENSOR_IDs = 4, 5
        SENSOR_INVERSIONS = True, True

        ENCODER_COUNTS_PER_DEGREE = 1000
        ANGLE_MIN_DEGREES = -130
        ANGLE_MAX_DEGREES = 130

        CALIBRATION_SPEED = 0.01
        POSITIVE_SPEED_CLOCKWISE = True

        PID = PIDConfiguration()
        PIDTolerance = PIDSetpointConfiguration()
        FeedForward = FeedForwardConfiguration()
        HeadingFeedForward = 0

    class Hood(ConstantsClass):
        MOTOR_IDs = -6
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
