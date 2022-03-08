import collections
import constants

from . import _feeder
from . import _turret
from . import _hood
from . import _josh

feeder = _feeder.Feeder()
turret = _turret.Turret()
hood = _hood.Hood(
    constants.Shooter.Hood.MOTOR_IDs,
)
mo = _josh.Josh(
    constants.Shooter.Josh.Mo.MOTOR_IDs,
    constants.Shooter.Josh.Mo.SPEED_INCREASE_FACTOR,
    constants.Shooter.Josh.Mo.MOTOR_CONFIG
)
mo.setName('Mo')
lester = _josh.Josh(
    constants.Shooter.Josh.Lester.MOTOR_IDs,
    constants.Shooter.Josh.Lester.SPEED_INCREASE_FACTOR,
    constants.Shooter.Josh.Lester.MOTOR_CONFIG
)
lester.setName('Lester')
