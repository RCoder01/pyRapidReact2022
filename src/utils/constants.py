from __future__ import annotations
import typing
import warnings

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
