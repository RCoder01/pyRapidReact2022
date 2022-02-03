import math
import commands2
from networktables import NetworkTables
from wpilib import SmartDashboard

import constants


class Limelight(commands2.SubsystemBase):
    """
    This subsystem is not intended to be required by any command.
    """
    def periodic(self) -> None:
        SmartDashboard.putNumberArray(
            "Limelight XYAV",
            [self.tx, self.ty, self.ta, self.tv]
        )
        return super().periodic()

    def __init__(self):
        commands2.SubsystemBase.__init__(self)

        self._table = NetworkTables.getTable('limelight')
        self._table.getEntry('pipeline').setDouble(1)
        self._table.getEntry('ledMode').setDouble(3)

    @property
    def tx(self):
        """The horizontal offset from crosshair to target."""
        return self._table.getNumber('tx', None) or 0

    @property
    def ty(self):
        """The vertical offset from crosshair to target."""
        return self._table.getNumber('ty', None) or 0

    @property
    def ta(self):
        """The relative size (distance) of the target."""
        return self._table.getNumber('ta', None) or 0

    @property
    def tv(self):
        """The number of targets being tracked (0 or 1)."""
        return self._table.getNumber('tv', None) or 0

    @property
    def x(self):
        """The normalized horizontal distance to the target."""
        return 0

    @property
    def y(self):
        """The normalized vertical distance to the target."""
        return math.sin(self.ty + constants.Limelight.MOUNT_ANGLE)

    @property
    def z(self):
        """The normalized forward distance to the target."""
        return math.cos(self.ty + constants.Limelight.MOUNT_ANGLE)
