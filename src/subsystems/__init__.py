"""All of the robots publicly accessible subsystems."""
import constants

from . import _drivetrain
from . import _belt
from . import _limelight
from . import _intake
from . import shooter

drivetrain = _drivetrain.Drivetrain(
    constants.Drivetrain.LeftMotors.IDs,
    constants.Drivetrain.RightMotors.IDs,
    constants.Drivetrain.ENCODER_COUNTS_PER_METER,
)

limelight = _limelight.Limelight()

intake = _intake.Intake(
    constants.Intake.MOTOR_IDs,
)

belt = _belt.Belt(
    constants.Belt.MOTOR_IDs,
    constants.Belt.IN_SENSOR_IDs,
    constants.Belt.OUT_SENSOR_IDs,
)
