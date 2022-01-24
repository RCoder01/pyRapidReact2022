import commands2
from networktables import NetworkTables
from wpilib import SmartDashboard


class Limelight(commands2.SubsystemBase):
    
    def periodic(self) -> None:
        SmartDashboard.putNumberArray(
            "Limelight XYAV",
            [self.tx, self.ty, self.ta, self.tv]
        )
        super().periodic()
    
    def __init__(self):
        self._table = NetworkTables.getTable("limelight")
        self._table.getEntry("pipeline").setNumber(1)
        self._table.getEntry("ledMode").setNumber(3)

        super().__init__()

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