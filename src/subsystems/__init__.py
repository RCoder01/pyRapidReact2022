"""All of the robots publicly accessible subsystems."""
import constants

from . import _drivetrain
from . import _limelight
from . import _intake
from . import shooter

drivetrain = _drivetrain.Drivetrain(
    constants.Drivetrain.LeftMotor.IDs,
    constants.Drivetrain.RightMotor.IDs,
    constants.Drivetrain.GYRO_PORT,
    constants.Drivetrain.ENCODER_COUNTS_PER_METER,    
)

limelight = _limelight.Limelight()

intake = _intake.Intake(
    constants.Intake.MOTOR_IDs,
)
