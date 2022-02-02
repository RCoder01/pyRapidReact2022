from re import S
import ctre
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
    
    ENCODER_COUNTS_PER_ROTATION = 2048
    ENCODER_COUNTS_PER_METER = 3000

    class Characterization(ConstantsClass):

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
    IDs = 5,
    DEFAULT_INTAKE_SPEED = 1


class Limelight(ConstantsClass):
    MOUNT_ANGLE = 0

    class PID(ConstantsClass):
        P = 0
        I = 0
        D = 0

    Ka = 0

    DEFAULT_ROTATION_SPEED = 0


class Shooter(ConstantsClass):
    IDs = 6,
    DEFAULT_SHOOTER_SPEED = 0
    MAX_VELOCITY_RPM = 5000

    class PID(ConstantsClass):
        P = 0.5
        I = 0.5
        D = 0.5


class Misc(ConstantsClass):
    SIMULATION_PERIOD_MS = 20
    MAX_VOLTAGE = 12
