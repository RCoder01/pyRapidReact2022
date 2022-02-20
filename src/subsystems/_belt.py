import typing
import warnings

import commands2
import wpilib

import utils.motor
import utils.sensor
import utils.warnings


class Belt(commands2.SubsystemBase):
    def periodic(self) -> None:
        wpilib.SmartDashboard.putBoolean('Belt In Sensor', self.get_in_sensor())
        wpilib.SmartDashboard.putBoolean('Belt In Sensor Disagreement', bool(self._in_sensor.get_error_state()))
        wpilib.SmartDashboard.putBoolean('Belt Out Sensor', self.get_out_sensor())
        wpilib.SmartDashboard.putBoolean('Belt Out Sensor Disagreement', bool(self._out_sensor.get_error_state()))

    def __init__(
            self,
            motor_IDs: typing.Collection[float],
            in_sensor_IDs: tuple[int, int],
            out_sensor_ID: tuple[int, int],
            ) -> None:
        commands2.SubsystemBase.__init__(self)
        self.setName('Belt')

        self._in_sensor = utils.sensor.DoubleDigitialInput(*in_sensor_IDs, False, True)
        self._out_sensor = utils.sensor.DoubleDigitialInput(*out_sensor_ID, False, True)

        self._motor_group = utils.motor.HeadedDefaultMotorGroup(motor_IDs)

        self.set_speed(0)

    def set_speed(self, speed: float):
        """Set the speed of the feeder motors."""
        self._motor_group.set_output(speed)
    
    def get_current_speed(self):
        """Return the current speed of the feeder motors."""
        return self._motor_group.get_lead_encoder_velocity()

    def get_in_sensor(self, strict: bool = False):
        """Return whether the first feeder sensor is active."""
        if self._in_sensor.get_error_state():
            warnings.warn('Belt in sensor disagreement', utils.warnings.LikelyHardwareError)
        return self._in_sensor.get_strict() if strict else self._in_sensor.get_leniant()

    def get_out_sensor(self, strict: bool = False):
        """Return whether the second feeder sensor is active."""
        if self._out_sensor.get_error_state():
            warnings.warn('Belt out sensor disagreement', utils.warnings.LikelyHardwareError)
        return self._out_sensor.get_strict() if strict else self._out_sensor.get_leniant()
