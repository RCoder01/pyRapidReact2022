import enum
import typing

import ctre

import constants


class CumulativeEncoder:
    def __init__(self, encoder_counts_per_rotation):
        self.ticks = 0
        self.delta = 0
        self.last_raw_ticks = 0
        self.ENCODER_COUNTS_PER_ROTATION = encoder_counts_per_rotation
    
    def update(self, raw_ticks: int, velocity_positive: bool) -> None:
        self.delta = raw_ticks - self.last_raw_ticks
        self.last_raw_ticks = raw_ticks
        self.delta += ((velocity_positive) + (self.delta < 0) - 1) * self.ENCODER_COUNTS_PER_ROTATION
        self.ticks += self.delta


class HeadedDefaultMotorGroup:

    ENCODER_COUNTS_PER_ROTATION: int = constants.Misc.ENCODER_COUNTS_PER_ROTATION

    def __init__(self, ID_List: typing.Collection[int], encoder_counts_per_rotation: int = None, inversions: typing.Collection[bool] = None) -> None:
        self.motors = [ctre.WPI_TalonFX(ID) for ID in ID_List]
        self.lead = self.motors[0]
        for motor in self.motors[1:]:
            motor.follow(self.lead)

        if inversions is None:
            for motor in self.motors[1:]:
                motor.setInverted(ctre.InvertType.FollowMaster)
        else:
            for motor, inverted in zip(self.motors, inversions):
                if inverted:
                    motor.setInverted(ctre.InvertType.FollowMaster)
                else:
                    motor.setInverted(ctre.InvertType.OpposeMaster)

        if encoder_counts_per_rotation is not None:
            self.ENCODER_COUNTS_PER_ROTATION = encoder_counts_per_rotation

    def get_lead_encoder_position(self):
        """Return the encoder position of the lead motor."""
        return self.lead.getSelectedSensorPosition() or 0

    def get_lead_encoder_velocity(self):
        """Return the encoder velocity of the lead motor."""
        return self.lead.getSelectedSensorVelocity() or 0

    def reset_lead_encoder(self):
        """Reset the encoder of the lead motor."""
        self.lead.setSelectedSensorPosition(0)

    def invert_all(self, inverted: bool = True):
        """Set the inversion of the motors."""
        self.lead.setInverted(inverted)

    def set_netural_mode_coast(self):
        """Set the motors so that tey coast when neutral."""
        self.lead.setNeutralMode(ctre.NeutralMode.Coast)
        for motor in self.motors:
            motor.setNeutralMode(ctre.NeutralMode.Coast)

    def set_netural_mode_brake(self):
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


class OdometricHeadedDefaultMotorGroup(HeadedDefaultMotorGroup):

    def __init__(self, ID_List: typing.Collection[int], conversion_factor: float = 1):
        super().__init__(ID_List)
        self._CONVERSION_FACTOR = conversion_factor

        self.reset_lead_encoder()

        self._cumulative_encoder = CumulativeEncoder(self.ENCODER_COUNTS_PER_ROTATION)

    def reset_lead_encoder(self):
        """Reset the encoder of the lead motor."""
        self._cumulative_encoder.last_raw_ticks = 0

        super().reset_lead_encoder()

    def reset_odometry(self):
        """
        Reset the cumulative and current encoder counts of the motors.

        Will likely break any discontinuous motion.

        :returns: The cumulative distance of the motors before being reset.
        """
        self.reset_lead_encoder()

        cum = self._cumulative_encoder.ticks
        self._cumulative_encoder.ticks = 0

        return cum * self._CONVERSION_FACTOR

    def periodic(self):
        """
        Update the cumulative encoder counts of the motors.

        Must be called periodically.
        """
        self._cumulative_encoder.update(self.get_lead_encoder_position(), self.get_lead_encoder_velocity())\

    def get_last_distance(self):
        """
        Return the distance traveled since the last reset.

        Calculated by the encoder ticks.
        """
        return self._cumulative_encoder.delta / self._CONVERSION_FACTOR

    def get_cumulative_distance(self):
        return self._cumulative_encoder.ticks


class ContinuousHeadedDefaultMotorGroup(OdometricHeadedDefaultMotorGroup):
    def __init__(self, ID_List: typing.Collection[int], conversion_factor: float = 1, min_cumulative_encoder_counts: int = 0, max_cumulative_encoder_counts: int = 0):
        super().__init__(ID_List, conversion_factor)

        self._MIN_CUMULATIVE_ENCODER_COUNTS = min_cumulative_encoder_counts
        self._MAX_CUMULATIVE_ENCODER_COUNTS = max_cumulative_encoder_counts

        if min_cumulative_encoder_counts > max_cumulative_encoder_counts:
            raise ValueError("min_cumulative_encoder_counts must be less than or equal to max_cumulative_encoder_counts")

    def periodic(self):
        super().periodic()

        if self._cumulative_encoder_ticks < self._MIN_CUMULATIVE_ENCODER_COUNTS:
            self._cumulative_encoder_ticks += (self._MAX_CUMULATIVE_ENCODER_COUNTS - self._MIN_CUMULATIVE_ENCODER_COUNTS)
        
        if self._cumulative_encoder_ticks > self._MAX_CUMULATIVE_ENCODER_COUNTS:
            self._cumulative_encoder_ticks -= (self._MAX_CUMULATIVE_ENCODER_COUNTS - self._MIN_CUMULATIVE_ENCODER_COUNTS)


class LimitedHeadedDefaultMotorGroup(OdometricHeadedDefaultMotorGroup):
    class Status(enum.Enum):
        AT_LOWER_LIMIT = -1
        WITHIN_BOUNDS = 0
        AT_UPPER_LIMIT = 1

    def __init__(self, ID_List: typing.Collection[int], conversion_factor: float = 1, min_cumulative_encoder_counts: int = 0, max_cumulative_encoder_counts: int = 0):
        super().__init__(ID_List, conversion_factor)

        self._MIN_CUMULATIVE_ENCODER_COUNTS = min_cumulative_encoder_counts
        self._MAX_CUMULATIVE_ENCODER_COUNTS = max_cumulative_encoder_counts

        if min_cumulative_encoder_counts >= max_cumulative_encoder_counts:
            raise ValueError("min_cumulative_encoder_counts must be less than max_cumulative_encoder_counts")

    def periodic(self):
        super().periodic()

        if self._cumulative_encoder.ticks <= self._MIN_CUMULATIVE_ENCODER_COUNTS:
            self.set_output(0)
            self.set_netural_mode_coast(ctre.NeutralMode.Coast)
            return self.Status.AT_LOWER_LIMIT

        if self._cumulative_encoder.ticks > self._MAX_CUMULATIVE_ENCODER_COUNTS:
            self.set_output(0)
            self.set_netural_mode_coast(ctre.NeutralMode.Coast)
            return self.Status.AT_UPPER_LIMIT

        self.set_netural_mode_coast(ctre.NeutralMode.Brake)
        return self.Status.WITHIN_BOUNDS
    
    def get_percent_limit(self):
        return (self._cumulative_encoder.ticks - self._MIN_CUMULATIVE_ENCODER_COUNTS) / (self._MAX_CUMULATIVE_ENCODER_COUNTS - self._MIN_CUMULATIVE_ENCODER_COUNTS)
