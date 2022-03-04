import constants

from . import _feeder
from . import _turret
# from . import _hood
from . import _josh

# feeder = _feeder.Feeder(
#     constants.Shooter.Feeder.MOTOR_IDs
# )
turret = _turret.Turret(
    constants.Shooter.Turret.MOTOR_IDs,
    constants.Shooter.Turret.ANGLE_MAX_DEGREES - constants.Shooter.Turret.ANGLE_MIN_DEGREES,
    constants.Shooter.Turret.ENCODER_COUNTS_PER_DEGREE,
)
# hood = _hood.Hood(
#     constants.Shooter.Hood.MOTOR_IDs,
#     min_encoder_counts=constants.Shooter.Hood.EncoderLimits.MIN,
#     max_encoder_counts=constants.Shooter.Hood.EncoderLimits.MAX,
# )
# lester = _josh.Josh(
#     constants.Shooter.Josh.Lester.MOTOR_IDs,
#     constants.Shooter.Josh.Lester.SPEED_DECREASE_FACTOR,
# )
# lester.setName('Lester')
# mo = _josh.Josh(
#     constants.Shooter.Josh.Mo.MOTOR_IDs,
#     constants.Shooter.Josh.Mo.SPEED_DECREASE_FACTOR,
# )
# mo.setName('Mo')
