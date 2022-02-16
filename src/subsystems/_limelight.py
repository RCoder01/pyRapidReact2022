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
        self._pipeline_entry = self._table.getEntry('pipeline')
        self._ledmode_entry = self._table.getEntry('ledMode')

        self._pipeline_entry.setDouble(constants.Limelight.PIPELINE)
        self._ledmode_entry.setDouble(0)

        self._MOUNT_ANGLE = constants.Limelight.MOUNT_ANGLE

    @property
    def tx(self):
        """The horizontal offset from crosshair to target."""
        return self._table.getNumber('tx', 0)

    @property
    def ty(self):
        """The vertical offset from crosshair to target."""
        return self._table.getNumber('ty', 0)

    @property
    def ta(self):
        """The relative size (distance) of the target."""
        return self._table.getNumber('ta', 0)

    @property
    def tv(self):
        """The number of targets being tracked (0 or 1)."""
        return self._table.getNumber('tv', 0)

    @property
    def y(self):
        """
        The normalized vertical distance to the target.

        Innacurate unless tx is 0
        """
        return math.sin(self.ty + self._MOUNT_ANGLE)

    @property
    def z(self):
        """
        The normalized forward distance to the target.

        Innacurate unless tx is 0
        """
        return math.cos(self.ty + self._MOUNT_ANGLE)

    @property
    def is_aligned(self):
        return self.tv == 1 and math.fabs(self.tx) < constants.Limelight.X_TOLERANCE

    def set_led_mode(self, mode: int):
        self._ledmode_entry.setDouble(mode)
