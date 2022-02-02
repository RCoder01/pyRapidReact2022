from __future__ import annotations
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
    def __init__(self, ID_List: typing.Collection[int]) -> None:
        self.motors = [ctre.WPI_TalonFX(ID) for ID in ID_List]
        self.lead = self.motors[0]
        for motor in self.motors[1:]:
            motor.follow(self.lead)

        self.lead_sensor_collection = self.lead.getSensorCollection()

    def get_lead_encoder_position(self):
        self.lead_sensor_collection.getIntegratedSensorPosition()

    def get_lead_encoder_velocity(self):
        self.lead_sensor_collection.getIntegratedSensorVelocity()

    def reset_lead_encoder(self):
        self.lead_sensor_collection.setIntegratedSensorPosition(0)

    def set_inverted(self, inverted: bool = True):
        for motor in self.motors:
            motor.setInverted(inverted)
