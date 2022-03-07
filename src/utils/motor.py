import abc
import enum
import typing

import ctre
import rev
import wpilib

import constants



class HeadedMotorGroup(abc.ABC):
    @abc.abstractmethod
    def __init__(self, motor_IDs: typing.Collection[int]) -> None: ...

    @abc.abstractmethod
    def invert_all(self, inverted: bool = True): ...

    @abc.abstractmethod
    def set_output(self, output: float): ...


class EncodedHeadedMotorGroup(HeadedMotorGroup):
    ENCODER_COUNTS_PER_ROTATION: int

    def set_soft_offset(self, encoder_count: int = 0):
        self._soft_offset = encoder_count

    def configure_units(self, encoder_counts_per_unit: float = 1) -> None:
        self._encoder_counts_per_unit = encoder_counts_per_unit

    @abc.abstractmethod
    def get_lead_encoder_position(self) -> int: ...

    def get_configured_lead_encoder_position(self):
        """Return the encoder position of the lead motor in configured units."""
        return self.get_lead_encoder_position() / self._encoder_counts_per_unit

    @abc.abstractmethod
    def reset_lead_encoder_position(self, new_position: int = 0) -> int: ...


class TalonFXGroup(EncodedHeadedMotorGroup):

    ENCODER_COUNTS_PER_ROTATION: int = constants.Misc.TALONFX_ENCODER_COUNTS_PER_ROTATION

    def __init__(self, ID_List: typing.Collection[int]) -> None:
        self.lead, *self.followers = self.motors = [ctre.WPI_TalonFX(ID) for ID in ID_List]
        for motor in self.followers:
            motor.follow(self.lead)
        for motor in self.motors:
            motor.configFactoryDefault()

        for motor in self.followers:
            motor.setInverted(ctre.InvertType.FollowMaster)

        self._RPM_CONVERSION_FACTOR = 10 * 60 / self.ENCODER_COUNTS_PER_ROTATION

        self.reset_lead_encoder_position()

        self.set_soft_offset()
        self.configure_units()

    def get_lead_encoder_position(self):
        """Return the raw encoder position of the lead motor."""
        return self.lead.getSelectedSensorPosition() + self._soft_offset or 0

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
    
    def _set_with_arbitrary_feeforward(self, control_type, value, feedforward):
        self.lead.set(control_type, value, ctre.DemandType.ArbitraryFeedForward, feedforward)

    def set_output(self, value: float, feedforward: float = 0):
        """Set the speed of the motors, using the default configuration."""
        self._set_with_arbitrary_feeforward(ctre.ControlMode.PercentOutput, value, feedforward)

    def set_velocity(self, target_velocity: float, feedforward: float = 0):
        """Set the velocity of the motors, using the default configuration."""
        self._set_with_arbitrary_feeforward(ctre.ControlMode.PercentOutput, target_velocity, feedforward)

    def set_configured_velocity(self, target_velocity: float, feedforward: float = 0):
        """Set the velocity of the motors in configured units/second."""
        self.set_velocity(target_velocity * self._encoder_counts_per_unit / 10, feedforward)

    def set_setpoint(self, target: int, feedforward: float = 0):
        """Set the setpoint of the lead motor."""
        self._set_with_arbitrary_feeforward(ctre.ControlMode.Position, target - self._soft_offset, feedforward)

    def set_configured_setpoint(self, configured_target: float, feedforward: float = 0):
        """Set the setpoint of the lead motor in configured units."""
        self.set_setpoint(int(configured_target * self._encoder_counts_per_unit + 0.5), feedforward)

    def get_output_voltage(self):
        """Return the current applied voltage of the lead motor."""
        return self.lead.getMotorOutputVoltage()


class TalonFXGroupSim():
    def __init__(self, motor_group: TalonFXGroup) -> None:
        self.motor_group = motor_group
        self.lead_sim_collection = self.motor_group.lead.getSimCollection()

    def set_raw_distance(self, distance: int):
        """Set the raw (simulated) distance of the lead motor."""
        self.lead_sim_collection.setIntegratedSensorRawPosition(distance)

    def set_configured_distance(self, distance: float):
        """Set the configured (simulated) distance of the lead motor."""
        self.set_raw_distance(int(distance * self.motor_group._encoder_counts_per_unit + 0.5))

    def set_raw_velocity(self, velocity: int):
        """Set the raw (simulated) velocity of the lead motor."""
        self.lead_sim_collection.setIntegratedSensorVelocity(velocity)

    def set_configured_velocity(self, velocity: float):
        """Set the configured (simulated) velocity of the lead motor."""
        self.set_raw_velocity(int(velocity * self.motor_group._encoder_counts_per_unit / 10 + 0.5))


class CANSparkMaxGroup(EncodedHeadedMotorGroup):
    ENCODER_COUNTS_PER_ROTATION = 1

    def __init__(
            self,
            motor_IDs: typing.Collection[int],
            motor_type: rev.CANSparkMax.MotorType = rev.CANSparkMax.MotorType.kBrushless
            ) -> None:
        self.lead, *self.followers = self.motors = [rev.CANSparkMax(ID, motor_type) for ID in motor_IDs]
        for motor in self.followers:
            motor.follow(self.lead)

        self.lead_encoder = self.lead.getEncoder()
        self.lead_PID_controller = self.lead.getPIDController()

    def invert_all(self, inverted: bool = True):
        self.lead.setInverted(inverted)

    def set_output(self, output: float):
        self.lead.set(output)

    def get_lead_encoder_position(self) -> int:
        """Return the encoder rotations of the lead motor."""
        return self.lead_encoder.getPosition()

    def get_lead_encoder_velocity(self) -> float:
        """Return the velocity of the lead motor in RPM."""
        return self.lead_encoder.getVelocity()
    
    def get_configured_lead_encoder_velocity(self):
        """Return the encoder velocity of the lead motor in configured units/second"""
        return self.get_lead_encoder_velocity / (self._encoder_counts_per_unit * 60)

    def reset_lead_encoder_position(self, new_position: int = 0) -> int:
        self.lead_encoder.setPosition(new_position)

    def set_setpoint(self, target: int):
        self.lead_PID_controller.setReference(target)


class LimitedHeadedDefaultMotorGroup(TalonFXGroup):
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
