import enum
import typing

import ctre
import wpilib

import constants


class HeadedDefaultMotorGroup:

    ENCODER_COUNTS_PER_ROTATION: int = constants.Misc.ENCODER_COUNTS_PER_ROTATION

    def __init__(
            self,
            ID_List: typing.Collection[int],
            encoder_counts_per_rotation: int = None,
            inversions: typing.Collection[bool] = None
            ) -> None:
        inversions = inversions or []
        self.motors = [ctre.WPI_TalonFX(ID) for ID in ID_List]
        self.lead = self.motors[0]
        for motor in self.motors[1:]:
            motor.follow(self.lead)
        for motor in self.motors:
            motor.configFactoryDefault()

        for motor in self.motors[1:]:
            motor.setInverted(ctre.InvertType.FollowMaster)
        for motor, inverted in zip(self.motors, inversions):
            if inverted:
                motor.setInverted(ctre.InvertType.OpposeMaster)

        if encoder_counts_per_rotation is not None:
            self.ENCODER_COUNTS_PER_ROTATION = encoder_counts_per_rotation

        self._RPM_CONVERSION_FACTOR = 10 * 60 / self.ENCODER_COUNTS_PER_ROTATION

        self.reset_lead_encoder_position()

        self.set_soft_offset()
        self.configure_units(1)

    def set_soft_offset(self, encoder_counts: int = 0):
        self._soft_offset = encoder_counts

    def configure_units(self, encoder_counts_per_unit: int):
        """Configure custom encoder units."""
        self._encoder_counts_per_unit = encoder_counts_per_unit

    def get_lead_encoder_position(self):
        """Return the raw encoder position of the lead motor."""
        return self.lead.getSelectedSensorPosition() + self._soft_offset or 0

    def get_configured_lead_encoder_position(self):
        return self.get_lead_encoder_position() / self._encoder_counts_per_unit

    def get_lead_encoder_velocity(self):
        """Return the raw encoder velocity of the lead motor."""
        return self.lead.getSelectedSensorVelocity() or 0

    def get_configured_lead_encoder_velocity(self):
        """Return the encoder velocity of the lead motor in configured units/second"""
        return self.get_lead_encoder_velocity() * 10 / self._encoder_counts_per_unit

    def reset_lead_encoder_position(self, new_position: int = 0):
        """Reset the encoder of the lead motor."""
        self.lead.setSelectedSensorPosition(new_position)

    def invert_all(self, inverted: bool = True):
        """Set the inversion of the motors."""
        self.lead.setInverted(inverted)

    def set_neutral_mode_coast(self):
        """Set the motors so that tey coast when neutral."""
        self.lead.setNeutralMode(ctre.NeutralMode.Coast)
        for motor in self.motors:
            motor.setNeutralMode(ctre.NeutralMode.Coast)

    def set_neutral_mode_brake(self):
        """Set the motors so that they brake when neutral."""
        self.lead.setNeutralMode(ctre.NeutralMode.Brake)
        for motor in self.motors:
            motor.setNeutralMode(ctre.NeutralMode.Brake)

    def set_output(self, value: float):
        """
        Set the speed of the motors, using the default configuration.

        :param value: The speed to set the motors to, ranging from -1 to 1.
        """
        self.lead.set(ctre.ControlMode.PercentOutput, value)

    def set_velocity(self, target_velocity: float):
        """Set the velocity of the motors, using the default configuration."""
        self.lead.set(ctre.ControlMode.Velocity, target_velocity)

    def set_configured_velocity(self, target_velocity: float):
        """Set the velocity of the motors in configured units/second."""
        self.set_velocity(target_velocity * self._encoder_counts_per_unit / 10)

    def set_setpoint(self, target: int):
        self.lead.set(ctre.ControlMode.Position, target - self._soft_offset)

    def set_configured_setpoint(self, configured_target: float):
        self.set_setpoint(int(configured_target * self._encoder_counts_per_unit + 0.5))

    def get_output_voltage(self):
        return self.lead.getMotorOutputVoltage()


class HeadedDefaultMotorGroupSim():
    def __init__(self, motor_group: HeadedDefaultMotorGroup) -> None:
        self.motor_group = motor_group
        self.lead_sim_collection = self.motor_group.lead.getSimCollection()

    def set_raw_distance(self, distance: int):
        self.lead_sim_collection.setIntegratedSensorRawPosition(distance)

    def set_configured_distance(self, distance: float):
        self.set_raw_distance(int(distance * self.motor_group._encoder_counts_per_unit + 0.5))

    def set_raw_velocity(self, velocity: int):
        self.lead_sim_collection.setIntegratedSensorVelocity(velocity)

    def set_configured_velocity(self, velocity: float):
        self.set_raw_velocity(int(velocity * self.motor_group._encoder_counts_per_unit / 10 + 0.5))


class LimitedHeadedDefaultMotorGroup(HeadedDefaultMotorGroup):
    class Status(enum.Enum):
        AT_LOWER_LIMIT = -1
        WITHIN_BOUNDS = 0
        AT_UPPER_LIMIT = 1

    def __init__(
            self,
            ID_List: typing.Collection[int],
            min_limit: int | typing.Callable[[int], bool],
            max_limit: int | typing.Callable[[int], bool],
            encoder_counts_per_rotation: int = None,
            inversions: typing.Collection[bool] = None,
            ) -> None:
        super().__init__(ID_List, encoder_counts_per_rotation, inversions)

        self.status = self.Status.WITHIN_BOUNDS

        self._at_min_limit: typing.Callable[[int], bool] = lambda count: count < min_limit if isinstance(min_limit, int) else min_limit
        self._at_max_limit: typing.Callable[[int], bool] = lambda count: count < max_limit if isinstance(max_limit, int) else max_limit

    def get_status(self):
        position = self.get_lead_encoder_position()

        if self._at_min_limit(position):
            self.status = self.Status.AT_LOWER_LIMIT
        elif self._at_max_limit(position):
            self.status = self.Status.AT_UPPER_LIMIT
        else:
            self.status = self.Status.WITHIN_BOUNDS

        return self.status

    def set_output(self, value: float):
        if self.status == self.Status.AT_LOWER_LIMIT and value < 0:
            return
        if self.status == self.Status.AT_UPPER_LIMIT and value > 0:
            return
        return super().set_output(value)
