from __future__ import annotations
import math
import typing

import wpimath.geometry

class HeadingFeedForward:
    def __init__(self, kP=1, last_robot_position: wpimath.geometry.Pose2d = wpimath.geometry.Pose2d()) -> None:
        self._kP = kP
        self._last_robot_position = last_robot_position

    def __call__(self, robot_position: wpimath.geometry.Pose2d) -> float:
        """Extrapolate past and current robot positions to calculate natural change in field-relative angle."""
        return (
            robot_position.relativeTo(robot_position.exp(self._last_robot_position.log(robot_position))).rotation().degrees() \
            - robot_position.rotation().degrees() \
            * self._kP
        )
    
    def calculate(self, robot_position: wpimath.geometry.Pose2d) -> float:
        """Extrapolate past and current robot positions to calculate natural change in field-relative angle."""
        return self(robot_position)

# TODO: Add vector3D
class Vector3D:
    def __init__(self, x: float = 0, y: float = 0, z: float = 0) -> None:
        self.x = x
        self.y = y
        self.z = z

    @staticmethod
    def from_shperical(r: float, theta: float, phi: float) -> Vector3D:
        return Vector3D(
            r * math.sin(theta) * math.cos(phi),
            r * math.sin(theta) * math.sin(phi),
            r * math.cos(theta)
        )

    @staticmethod
    def from_cartesian(x: float, y: float, z: float) -> Vector3D:
        return Vector3D(x, y, z)

    @property
    def magnitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    @magnitude.setter
    def magnitude(self, value: float) -> None:
        self.normalize()
        self.x *= value
        self.y *= value
        self.z *= value

    r = magnitude

    @property
    def phi(self) -> float:
        return math.atan2(self.y, self.x)

    @phi.setter
    def phi(self, value: float) -> None:
        self.xyz = self.__class__.from_shperical(self.r, self.theta, value)

    @property
    def theta(self) -> float:
        return math.acos(self.z / self.r)

    @theta.setter
    def theta(self, value: float) -> None:
        self.xyz = self.__class__.from_shperical(self.r, value, self.phi)

    def normalize(self) -> Vector3D:
        magnitude = self.magnitude
        self.xyz = self / magnitude
        return self
    
    @property
    def horizontal(self) -> Vector3D:
        return Vector3D(*self.xy, 0)

    def __str__(self) -> str:
        return f'[{self.x}, {self.y}, {self.z}]'

    def __repr__(self) -> str:
        return f'Vector3D({self.x}, {self.y}, {self.z})'

    def __add__(self, other: Vector3D) -> Vector3D:
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vector3D) -> Vector3D:
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other: Vector3D) -> Vector3D:
        return Vector3D(self.x * other.x, self.y * other.y, self.z * other.z)

    def __truediv__(self, other: Vector3D) -> Vector3D:
        return Vector3D(self.x / other.x, self.y / other.y, self.z / other.z)

    def __neg__(self) -> Vector3D:
        return Vector3D(-self.x, -self.y, -self.z)

    def __abs__(self) -> Vector3D:
        return Vector3D(abs(self.x), abs(self.y), abs(self.z))

    def __pow__(self, power: int) -> Vector3D:
        return Vector3D(self.x ** power, self.y ** power, self.z ** power)

    def __eq__(self, other: Vector3D) -> bool:
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __ne__(self, other: Vector3D) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def __getitem__(self, index: int | str) -> float:
        if isinstance(index, int):
            return (self.x, self.y, self.z)[index]  
        elif isinstance(index, str):
            return getattr(self, index)
        else:
            raise TypeError(f'Index must be an int or str, not {type(index)}')

    def __setitem__(self, index: int | str | tuple[int | str, ...], value: float) -> None:
        if isinstance(index, int):
            return setattr(self, ('x', 'y', 'z')[index], value)
        return self.__setattr__(index, value)

    def __getattr__(self, name: str) -> float:
        try:
            return tuple(getattr(self, char) for char in name if char in ('x', 'y', 'z'))
        except AttributeError as e:
            raise AttributeError(f'{type(self)} object has no attribute {name}') from e

    def __setattr__(self, name: str, value: float | tuple) -> None:
        try:
            return super().__setattr__(name, value)
        except AttributeError:
            pass

        if {'x', 'y', 'z'}.issuperset(name):
            for char in name:
                setattr(self, char, value)

    def __iter__(self) -> typing.Iterator[float]:
        yield self.x
        yield self.y
        yield self.z

    def __bool__(self) -> bool:
        return self != Vector3D()

    def __round__(self, n: int = 0) -> Vector3D:
        return Vector3D(round(self.x, n), round(self.y, n), round(self.z, n))

    def __floor__(self) -> Vector3D:
        return Vector3D(math.floor(self.x), math.floor(self.y), math.floor(self.z))

    def __ceil__(self) -> Vector3D:
        return Vector3D(math.ceil(self.x), math.ceil(self.y), math.ceil(self.z))

    def __trunc__(self) -> Vector3D:
        return Vector3D(math.trunc(self.x), math.trunc(self.y), math.trunc(self.z))

    def dot(self, other: Vector3D) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: Vector3D) -> Vector3D:
        return Vector3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )
