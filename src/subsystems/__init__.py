"""All of the robots publicly accessible subsystems."""
import constants

from . import _drivetrain
from . import _feeder
from . import _limelight
from . import _intake
from . import shooter

drivetrain = _drivetrain.Drivetrain(
    constants.Drivetrain.LeftMotors.IDs,
    constants.Drivetrain.RightMotors.IDs,
    constants.Drivetrain.GYRO_PORT,
    constants.Drivetrain.ENCODER_COUNTS_PER_METER,
    None,
    constants.Drivetrain.ENCODER_SPEED_TO_REAL_SPEED,
    constants.Drivetrain.ENCODER_SPEED_TO_REAL_SPEED,
)

limelight = _limelight.Limelight()

intake = _intake.Intake(
    constants.Intake.MOTOR_IDs,
)

feeder = _feeder.Feeder(
    constants.Feeder.TopMotors.IDs,
    constants.Feeder.BottomMotors.IDs,
    constants.Feeder.IN_SENSOR_IDs,
    constants.Feeder.OUT_SENSOR_IDs,
)
