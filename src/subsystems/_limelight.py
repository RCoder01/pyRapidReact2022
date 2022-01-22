import commands2
from networktables import NetworkTables
from wpilib import SmartDashboard


class Limelight(commands2.Subsystem):
    def __init__(self):
        self._table = NetworkTables.getTable("limelight")
        self._table.getEntry("pipeline").setNumber(1)
        self._table.getEntry("ledMode").setNumber(3)
    
    def periodic(self) -> None:
        SmartDashboard.putNumberArray(
            "Limelight XYAV",
            [self.tx, self.ty, self.ta, self.tv]
        )

    @property
    def tx(self):
        return self._table.getNumber('tx', None)
    
    @property
    def ty(self):
        return self._table.getNumber('ty', None)
    
    @property
    def ta(self):
        return self._table.getNumber('ta', None)
    
    @property
    def tv(self):
        return self._table.getNumber('tv', None)