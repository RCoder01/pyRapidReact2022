import enum

import wpilib


class DoubleDigitialInput:
    class Error(enum.Enum):
        AGREE = 0
        DISAGREE = 1

    def __init__(self, sensor_1_ID: int, sensor_2_ID: int, sensor_1_inverted: bool, sensor_2_inverted: bool):
        if not wpilib.RobotBase.isSimulation:
            self._sensor_1 = wpilib.DigitalInput(sensor_1_ID)
            self._sensor_2 = wpilib.DigitalInput(sensor_2_ID)
        else:
            self._sensor_1 = None
            self._sensor_2 = None
        self._sensor_1_inverted = bool(sensor_1_inverted)
        self._sensor_2_inverted = bool(sensor_2_inverted)

    @property
    def sensor1_active(self):
        if self._sensor_1 is None: return None
        return self._sensor_1.get() ^ self._sensor_1_inverted

    @property
    def sensor2_active(self):
        if self._sensor_2 is None: return None
        return self._sensor_2.get() ^ self._sensor_2_inverted

    def get_leniant(self):
        return self.sensor1_active or self.sensor2_active

    def get_strict(self):
        return self.sensor1_active and self.sensor2_active

    def get_error_state(self):
        return self.Error(int(bool(self.get_leniant() and not self.get_strict())))
