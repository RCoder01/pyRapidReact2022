import constants

from . import _turret
from . import _hood
from . import _josh

turret = _turret.Turret(
    constants.Shooter.Turret.MOTOR_IDs,
    constants.Shooter.Turret.CONTINUOUS_MAX_CUMULATIVE_ENCODER_COUNTS,
    constants.Shooter.Turret.ANGLE_RANGE_DEGREES
)
hood = _hood.Hood(
    constants.Shooter.Hood.MOTOR_IDs,
    min_encoder_counts=constants.Shooter.Hood.EncoderLimits.MIN,
    max_encoder_counts=constants.Shooter.Hood.EncoderLimits.MAX,
)
lester = _josh.Josh(
    constants.Shooter.Josh.Mo.MOTOR_IDs,
)
mo = _josh.Josh(
    constants.Shooter.Josh.Lester.MOTOR_IDs,
)
