"""All of the robots publicly accessible subsystems."""
import constants

from . import _drivetrain
from . import _belt
from . import _limelight
from . import _intake
from . import shooter

drivetrain = _drivetrain.Drivetrain()

limelight = _limelight.Limelight()

intake = _intake.Intake()

belt = _belt.Belt()
