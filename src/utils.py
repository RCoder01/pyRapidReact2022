from __future__ import annotations
import enum
import warnings
import typing
import math

import ctre

import constants


def deadzone(
        input,
        power=2,
        lower_maxzone=-1,
        lower_deadzone=-0.1,
        higher_deadzone=0.1,
        higher_maxzone=1,
        ):
    """
    Highly customizable deadzone function, 
    Follows equations at https://www.desmos.com/calculator/yt5brsfh1m

    :param input:
    The value to be set into deadzone
    :param power:
    The power to which the function should be taken;
    1 is linear, 2 is quadratic, etc.
    :param lower_maxzone:
    The negative point past which all inputs return -1
    :param lower_deadzone:
    The negative point past which all less inputs return 0
    :param higher_deadzone:
    The positive point past which all less inputs return 0
    :param higher_maxzone:
    The positive point at which all past inputs return 1

    :returns:
    Input modified by the different parameters

    Values must follow:
    -1 <= lower_maxzone < lower_deadzone <= 0
    <= higher_deadzone < higher_maxzone <= 1
    or ValueError will be raised
    """
    if not(
        -1 <= lower_maxzone < lower_deadzone <= 0
        <= higher_deadzone < higher_maxzone <= 1
    ):
        raise ValueError(
            'The following must be true: '
            '-1 <= lower_maxzone < lower_deadzone <= 0'
            '<= higher_deadzone < higher_maxzone <= 1'
        )
    if not(power >= 0):
        raise ValueError('Power must be greater than or equal to zero')

    # Depedning on range, use a different output formula
    if input <= lower_maxzone:
        return -1
    if lower_maxzone < input < lower_deadzone:
        return -math.pow(
            (-input + lower_deadzone) / (lower_deadzone - lower_maxzone),
            power,
        )
    if lower_deadzone <= input <= higher_deadzone:
        return 0
    if higher_deadzone < input < higher_maxzone:
        return math.pow(
            (input - higher_deadzone) / (higher_maxzone - higher_deadzone),
            power,
        )
    if higher_maxzone <= input:
        return 1


class NonwritableType(type):
    """
    When as metaclass, prevents any attribute from being set or deleted\n
    Mutable atttributes can still be modifed\n
    In the event an attribute must be modified, 
    'object.__setattr__(object, name, value)' or 
    'object.__delattr__(object, name)'
    can be used
    """
    __slots__ = ()

    def __setattr__(self, name: str, value) -> None:
        raise TypeError('Nonwritable attributes cannot be set')

    def __delattr__(self, name: str) -> None:
        raise TypeError('Nonwritable attributes cannot be deleted')


def remove_dunder_attrs(dict_: dict) -> dict:
    return {k: v for k, v in dict_.items() if not(k.startswith('__') and k.endswith('__'))}


class ConstantsType(NonwritableType):
    """Defines a get item and repr method"""
    def __new__(mcls: ConstantsType, clsname: str, bases: tuple, clsdict: dict) -> ConstantsType:
        """
        Checks for potentially dubious keys attribute
        and
        replaces annotation-only values with default values
        """

        if 'keys' in clsdict:
            warnings.warn('Defining a keys attribute may cause issues with "**" unpacking syntax', UserWarning)

        annotations = clsdict.get('__annotations__', {})
        for name, type_ in annotations.items():
            if name not in clsdict:
                type_ = eval(type_)

                err_text = f'{name} is only outlined in {clsname} as {type_!s} (not defined)'

                try:
                    annotation = annotation()
                except TypeError:
                    pass
                else:
                    err_text += f', replacing with default constructor value of {annotation!s}'

                warnings.warn(err_text, UserWarning)

                clsdict[name] = annotation

        return super().__new__(mcls, clsname, bases, clsdict)

    @typing.overload
    def __getitem__(self, name: str) -> typing.Any:
        """Get item from key"""

    @typing.overload
    def __getitem__(self, name: tuple[str]) -> typing.Any:
        """Get nested item from tuple of keys"""

    def __getitem__(self, name) -> typing.Any:
        if not isinstance(name, (str, tuple)):
            raise TypeError(f'Items must be of type str or tuple[str], not {type(name)}')

        try:
            if name in self.__dict__:
                return getattr(self, name)
            # If name is a tuple, iterate over sub-objects and their attributes
            if isinstance(name, tuple):
                obj = self

                for item in name:
                    # If it has items, check only those
                    # Otherwise, check attributes
                    if hasattr(obj, '__getitem__'):
                        obj = obj[item]
                    else:
                        obj = getattr(obj, item)

        except AttributeError as e:
            raise KeyError(*e.args) from e
        except KeyError:
            raise
        else:
            return obj

    # Taken practically directly from types.SimpleNamespace documentation page
    def __repr__(self) -> str:
        return f'{self.__name__}({", ".join([f"{k}={v!r}" for k, v in remove_dunder_attrs(self.__dict__).items()])})'

    def keys(self) -> tuple:
        return tuple(k for k, _ in remove_dunder_attrs(self.__dict__).items())

    def values(self) -> tuple:
        return tuple(v for k, v in remove_dunder_attrs(self.__dict__).items())

    def items(self) -> tuple:
        return tuple((k, v) for k, v in remove_dunder_attrs(self.__dict__).items())

    def __iter__(self) -> typing.Iterator[str]:
        return self.keys().__iter__()


class ConstantsClass(metaclass=ConstantsType):
    """
    Unique properties of a ConstantsClass:

    - Any class attributes cannot be changed or deleted;
    new class attributes cannot be added

    - Values can be accessed using the following notations: 
    ConstantsClass[key],
    ConstantsClass.key

    - Nested values can be accessed with the following notations
    if a class contains a nested class that inherits from ConstantsClass
    (works for more than two as well):
    ConstantsClass[key1][key2],
    ConstantsClass[key1, key2],
    ConstantsClass[(key1, key2)],
    ConstantsClass.key1.key2

    - Initializing a class returns the class itself, not an instance

    - Provides a useful repr;
    similar to that of types.SimpleNamespace,
    but ignores attributes with both two leading and underscores 
    ('dunder' attributes)
    """
    __slots__ = ()

    def __new__(cls: ConstantsClass) -> ConstantsClass:
        return cls


class HeadedDefaultMotorGroup:

    ENCODER_COUNTS_PER_ROTATION: int = constants.Misc.ENCODER_COUNTS_PER_ROTATION

    def __init__(self, ID_List: typing.Collection[int], encoder_counts_per_rotation: int = None) -> None:
        self.motors = [ctre.WPI_TalonFX(ID) for ID in ID_List]
        self.lead = self.motors[0]
        for motor in self.motors[1:]:
            motor.follow(self.lead)

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

    def set_inverted(self, inverted: bool = True):
        """Set the inversion of the motors.""" # TODO: Ensure implementation is accurate
        for motor in self.motors:
            motor.setInverted(inverted)

    def set_speed(self, value: float):
        """Set the speed of the motors, using the default configuration."""
        self.lead.set(ctre.ControlMode.PercentOutput, value)

    def set_velocity(self, target_velocity: float):
        """Set the velocity of the motors, using the default configuration."""
        self.lead.set(ctre.ControlMode.Velocity, target_velocity)


class OdometricHeadedDefaultMotorGroup(HeadedDefaultMotorGroup):

    def __init__(self, ID_List: typing.Collection[int], conversion_factor: float = 1):
        super().__init__(ID_List)
        self._CONVERSION_FACTOR = conversion_factor

        self.reset_lead_encoder()

        self._cumulative_encoder_ticks = 0
        self._last_raw_encoder_ticks = 0
        self._encoder_delta = 0

    def reset_lead_encoder(self):
        """Reset the encoder of the lead motor."""
        self._last_raw_encoder_ticks = 0

        super().reset_lead_encoder()

    def reset_odometry(self):
        """
        Reset the cumulative and current encoder counts of the motors.

        Will break any discontinuous motion.

        :returns: The cumulative distance of the motors before being reset.
        """
        self.reset_lead_encoder()

        cum = self._cumulative_encoder_ticks
        self._cumulative_encoder_ticks = 0

        return cum * self._CONVERSION_FACTOR

    def periodic(self):
        """
        Update the cumulative encoder counts of the motors.

        Must be called periodically.
        """
        raw_encoder_ticks: int = self.get_lead_encoder_position()

        self._encoder_delta = raw_encoder_ticks - self._last_raw_encoder_ticks

        self._last_raw_encoder_ticks = raw_encoder_ticks

        self._encoder_delta += ((self.get_lead_encoder_velocity() > 0) + (self._encoder_delta < 0) - 1) * self.ENCODER_COUNTS_PER_ROTATION

        self._cumulative_encoder_ticks += self._encoder_delta

    def get_last_distance(self):
        """
        Return the distance traveled since the last reset.

        Calculated by the encoder ticks.
        """
        return self._encoder_delta / self._CONVERSION_FACTOR
    
    def get_cumulative_distance(self):
        return self._cumulative_encoder_ticks


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

        if min_cumulative_encoder_counts > max_cumulative_encoder_counts:
            raise ValueError("min_cumulative_encoder_counts must be less than or equal to max_cumulative_encoder_counts")

    def periodic(self):
        super().periodic()

        if self._cumulative_encoder_ticks <= self._MIN_CUMULATIVE_ENCODER_COUNTS:
            self.set_speed(0)
            self.lead.setNeutralMode(ctre.NeutralMode.Coast)
            return self.Status.AT_LOWER_LIMIT

        if self._cumulative_encoder_ticks > self._MAX_CUMULATIVE_ENCODER_COUNTS:
            self.set_speed(0)
            self.lead.setNeutralMode(ctre.NeutralMode.Coast)
            return self.Status.AT_UPPER_LIMIT

        self.lead.setNeutralMode(ctre.NeutralMode.Brake)
        return self.Status.WITHIN_BOUNDS
