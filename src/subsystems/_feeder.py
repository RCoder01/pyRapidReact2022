import typing
import warnings

import commands2
import wpilib

import utils.motor
import utils.sensor


class Feeder(commands2.SubsystemBase):
    def periodic(self) -> None:
        wpilib.SmartDashboard.putBoolean('Feeder In Sensor', self.get_in_sensor())
        wpilib.SmartDashboard.putBoolean('Feeder In Sensor Disagreement', bool(self._in_sensor.get_error_state()))
        wpilib.SmartDashboard.putBoolean('Feeder Out Sensor', self.get_out_sensor())
        wpilib.SmartDashboard.putBoolean('Feeder Out Sensor Disagreement', bool(self._out_sensor.get_error_state()))

    def __init__(
            self,
            in_sensor_IDs: tuple[int, int],
            out_sensor_ID: tuple[int, int],
            bottom_motor_IDs: typing.Collection[float],
            top_motor_IDs: typing.Collection[float],
            ) -> None:
        commands2.SubsystemBase.__init__(self)
        self.setName('Feeder')

        self._in_sensor = utils.sensor.DoubleDigitialInput(*in_sensor_IDs)
        self._out_sensor = utils.sensor.DoubleDigitialInput(*out_sensor_ID)

        self._bottom_motor_group = utils.motor.HeadedDefaultMotorGroup(bottom_motor_IDs)
        self._top_motor_group = utils.motor.HeadedDefaultMotorGroup(top_motor_IDs)

        self.set_speeds(0)

    def set_speeds(self, bottom_speed: float, top_speed: float = None):
        """Set the speed of the feeder motors."""
        self._bottom_motor_group.set_output(bottom_speed)
        self._top_motor_group.set_output(top_speed or bottom_speed)

    def get_in_sensor(self, strict: bool = False):
        """Return whether the first feeder sensor is active."""
        if self._in_sensor.get_error_state():
            warnings.warn('Feeder in sensor disagreement')
        return self._in_sensor.get_strict() if strict else self._in_sensor.get_leniant()

    def get_out_sensor(self, strict: bool = False):
        """Return whether the second feeder sensor is active."""
        if self._out_sensor.get_error_state():
            warnings.warn('Feeder out sensor disagreement')
        return self._out_sensor.get_strict() if strict else self._out_sensor.get_leniant()
