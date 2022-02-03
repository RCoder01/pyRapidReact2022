import commands2

from . import _turret
from . import _hood
from . import _josh

turret = _turret.Turret()
hood = _hood.Hood()
mo = _josh.Josh()
lester = _josh.Josh()


class Shooter(commands2.SubsystemBase):
    pass
