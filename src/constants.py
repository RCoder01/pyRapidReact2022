import wpilib
from utils.constants import ConstantsClass

class Drivetrain(ConstantsClass):
    class LeftMotors(ConstantsClass):
        IDs = 0, 2

        class PID(ConstantsClass):
            P = 0
            I = 0 # Probably keep 0 (https://docs.wpilib.org/en/stable/docs/software/pathplanning/trajectory-tutorial/creating-following-trajectory.html)
            D = 0 # Probably keep 0

    class RightMotors(ConstantsClass):
        IDs = 1, 3

        class PID(ConstantsClass):
            P = 0
            I = 0 # Probably keep 0
            D = 0 # Probably keep 0
    
    ENCODER_COUNTS_PER_METER = 3000

    GYRO_PORT = wpilib.SPI.Port.kOnboardCS0 # TODO: Find which port the gyro is on

    ENCODER_SPEED_TO_REAL_SPEED = 10 / ENCODER_COUNTS_PER_METER # Encoder speed given in encoder counts per 100 ms

    class Characterization(ConstantsClass): # TODO: https://docs.wpilib.org/en/stable/docs/software/pathplanning/trajectory-tutorial/characterizing-drive.html

        class FeedForward(ConstantsClass):
            S = 0
            V = 0
            A = 0

        TRACK_WIDTH = 0.30 # meters

        MAX_SPEED = 0 # meters per second
        MAX_ACCELERATION = 0 # meters per second per second

        class Ramesete(ConstantsClass):
            B = 0
            ZETA = 0


class Feeder(ConstantsClass):
    class TopMotors(ConstantsClass):
        IDs = 5,
        DEFAULT_SPEED = 0.5
        DEFAULT_EXGEST_SPEED = -DEFAULT_SPEED

    class BottomMotors(ConstantsClass):
        IDs = 6,
        DEFAULT_SPEED = 0.5
        DEFAULT_EXGEST_SPEED = -DEFAULT_SPEED
    
    IN_SENSOR_IDs = 0, 1
    OUT_SENSOR_IDs = 2, 3


class Intake(ConstantsClass):
    MOTOR_IDs = 4,
    DEFAULT_INTAKE_SPEED = 0.1
    DEFAULT_EXGEST_SPEED = -DEFAULT_INTAKE_SPEED


class Limelight(ConstantsClass):
    MOUNT_ANGLE = 0

    class PID(ConstantsClass):
        P = 0
        I = 0
        D = 0

    Ka = 0

    PIPELINE = 1
    LED_MODE = 3

    X_TOLERANCE = 0.1


class Shooter(ConstantsClass):

    class PID(ConstantsClass):
        P = 0
        I = 0
        D = 0

    class Turret(ConstantsClass):
        MOTOR_IDs = 7,

        ENCODER_COUNTS_PER_ROTATION = 2048

        COVERAGE_AMOUNT = 1.00

        CONTINUOUS_MAX_CUMULATIVE_ENCODER_COUNTS = 2048 * (140*4 / 10) * COVERAGE_AMOUNT

        ANGLE_RANGE_DEGREES = 270

        class PID(ConstantsClass):
            P = 0
            I = 0
            D = 0

        class FeedForward(ConstantsClass):
            S = 0
            V = 0
            A = 0
            H = 0

    class Hood(ConstantsClass):
        MOTOR_IDs = 8,

        class EncoderLimits(ConstantsClass):
            MIN = 0
            MAX = 2048

        class PID(ConstantsClass):
            P = 0
            I = 0
            D = 0
    
    class Josh(ConstantsClass):

        class Mo(ConstantsClass):
            MOTOR_IDs = 9,

            class PID(ConstantsClass):
                P = 0
                I = 0
                D = 0

        class Lester(ConstantsClass):
            MOTOR_IDs = 10,

            class PID(ConstantsClass):
                P = 0
                I = 0
                D = 0


class Misc(ConstantsClass):
    SIMULATION_PERIOD_MS = 20
    MAX_VOLTAGE = 12

    ENCODER_COUNTS_PER_ROTATION = 2048

    MAX_VELOCITY_RPM = 5000

    class BallCounting(ConstantsClass):
        IN_DEBOUNCE_TIME = 0.1
        OUT_DEBOUNCE_TIME = 0.1

        MAX_CAPACITY = 2
