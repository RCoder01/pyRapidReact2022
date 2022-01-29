import math
import commands2
from networktables import NetworkTables
from wpilib import SmartDashboard

import constants


class Limelight(commands2.SubsystemBase):
    
    def periodic(self) -> None:
        SmartDashboard.putNumberArray(
            "Limelight XYAV",
            [self.tx, self.ty, self.ta, self.tv]
        )
        super().periodic()
    
    def __init__(self):
        commands2.SubsystemBase.__init__(self)

        self._table = NetworkTables.getTable("limelight")
        self._table.getEntry("pipeline").setDouble(1)
        self._table.getEntry("ledMode").setDouble(3)

    @property
    def tx(self):
        """The horizontal offset from crosshair to target."""
        return self._table.getNumber('tx', None)
    
    @property
    def ty(self):
        """The vertical offset from crosshair to target."""
        return self._table.getNumber('ty', None)
    
    @property
    def ta(self):
        """The relative size (distance) of the target."""
        return self._table.getNumber('ta', None)
    
    @property
    def tv(self):
        """The number of targets being tracked (0 or 1)."""
        return self._table.getNumber('tv', None)
    
    @property
    def x(self):
        return 0

    @property
    def y(self):
        return math.sin(self.ty + constants.Limelight.MOUNT_ANGLE)

    @property
    def z(self):
        return math.cos(self.ty + constants.Limelight.MOUNT_ANGLE)