"""All of the robots publicly accessible subsystems."""
from . import _drivetrain
from . import _limelight
from . import _intake
from . import _shooter

drivetrain = _drivetrain.Drivetrain()
limelight = _limelight.Limelight()
intake = _intake.Intake()
shooter = _shooter.Shooter()
