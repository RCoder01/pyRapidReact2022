from utils import (
    ConstantsClass
)

class DrivetrainConstants(ConstantsClass):
    class LeftMotor(ConstantsClass):
        IDs = (13, 14, 15)
        Kp = 0
        Ki = 0
        Kd = 0
    
    class RightMotor(ConstantsClass):
        IDs = (1, 2, 20)
        Kp = 0
        Ki = 0
        Kd = 0

class TeleopConstants(ConstantsClass):
    TARGET_SPEED = 0.5