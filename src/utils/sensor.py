import enum

import wpilib


class DoubleDigitialInput(wpilib.Sendable):
    class Error(enum.Enum):
        AGREE = 0
        DISAGREE = 1

    def __init__(self, sensor_1_ID: int, sensor_2_ID: int, sensor_1_inverted: bool, sensor_2_inverted: bool):
        self._sensor_1 = wpilib.DigitalInput(sensor_1_ID)
        self._sensor_2 = wpilib.DigitalInput(sensor_2_ID)
        self._sensor_1_inverted = bool(sensor_1_inverted)
        self._sensor_2_inverted = bool(sensor_2_inverted)

    @property
    def sensor1_active(self):
        return self._sensor_1.get() ^ self._sensor_1_inverted

    @property
    def sensor2_active(self):
        return self._sensor_2.get() ^ self._sensor_2_inverted

    def get_leniant(self):
        return self.sensor1_active or self.sensor2_active

    def get_strict(self):
        return self.sensor1_active and self.sensor2_active

    def get_error_state(self):
        return self.Error(self.get_leniant() and not self.get_strict())
