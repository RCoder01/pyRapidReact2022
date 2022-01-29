from utils import (
    ConstantsClass
)

class Drivetrain(ConstantsClass):
    class LeftMotor(ConstantsClass):
        IDs = 13, 14, 15

        class PID(ConstantsClass):
            P = 0
            I = 0
            D = 0
    
    class RightMotor(ConstantsClass):
        IDs = 1, 2, 20

        class PID(ConstantsClass):
            P = 0
            I = 0
            D = 0
    
    ENCODER_COUNTS_PER_FOOT = 0


class Intake(ConstantsClass):
    IDs = 0,
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
    IDs = 0,
    DEFAULT_SHOOTER_SPEED = 0

    class PID(ConstantsClass):
        P = 0
        I = 0
        D = 0