from re import S
import ctre
import wpilib
from utils import (
    ConstantsClass
)

class Drivetrain(ConstantsClass):
    class LeftMotor(ConstantsClass):
        IDs = 13, 14, 15

        class PID(ConstantsClass):
            P = 0
            I = 0 # Probably keep 0 (https://docs.wpilib.org/en/stable/docs/software/pathplanning/trajectory-tutorial/creating-following-trajectory.html)
            D = 0 # Probably keep 0
    
    class RightMotor(ConstantsClass):
        IDs = 1, 2, 20

        class PID(ConstantsClass):
            P = 0
            I = 0 # Probably keep 0
            D = 0 # Probably keep 0
    
    ENCODER_COUNTS_PER_METER = 3000

    GYRO_PORT = wpilib.SPI.Port # TODO: Find which port the gyro is on

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


class Intake(ConstantsClass):
    MOTOR_IDs = 5,
    DEFAULT_INTAKE_SPEED = 1


class Limelight(ConstantsClass):
    MOUNT_ANGLE = 0

    class PID(ConstantsClass):
        P = 0
        I = 0
        D = 0

    Ka = 0

    DEFAULT_ROTATION_SPEED = 0

    PIPELINE = 1
    LED_MODE = 3

    X_TOLERANCE = 0.1


class Shooter(ConstantsClass):
    IDs = 6,
    DEFAULT_SHOOTER_SPEED = 0
    MAX_VELOCITY_RPM = 5000

    class PID(ConstantsClass):
        P = 0
        I = 0
        D = 0
    
    class Turret(ConstantsClass):
        MOTOR_IDs = 7,

        ENCODER_COUNTS_PER_ROTATION = 2048

        class PID(ConstantsClass):
            P = 0
            I = 0
            D = 0

    class Hood(ConstantsClass):
        MOTOR_IDs = 8,

        class EncoderLimits(ConstantsClass):
            MIN = 0
            MAX = 2048

        class PID(ConstantsClass):
            P = 0
            I = 0
            D = 0

class Misc(ConstantsClass):
    SIMULATION_PERIOD_MS = 20
    MAX_VOLTAGE = 12

    ENCODER_COUNTS_PER_ROTATION = 2048