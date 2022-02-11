from __future__ import annotations

import math

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


class Vector2D:
    __slots__ = ('x', 'y')

    def __init__(self, initial_x: float = 0, initial_y: float = 0, initial_z: float = 0) -> None:
        self.x = initial_x
        self.y = initial_y
    
    @property
    def magnitude(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5
    
    @magnitude.setter
    def magnitude(self, value: float) -> float:
        if self.magnitude == 0:
            self.x = value
            return
        scale = value / self.magnitude
        self.x *= scale
        self.y *= scale
    
    @property
    def theta_radians(self) -> float:
        return math.atan2(self.y, self.x)
    
    @angle_radians.setter
    def angle_radians(self, value: float) -> None:
        magnitude = self.magnitude
        self.x = magnitude * math.cos(value)
        self.y = magnitude * math.sin(value)
    
    @property
    def angle_degrees(self) -> float:
        return math.degrees(self.angle_radians)
    
    @angle_degrees.setter
    def angle_degrees(self, value: float) -> None:
        self.angle_radians = math.radians(value)
    
    def copy(self):
        return Vector2D(self.x, self.y)
    
    def __add__(self, other: Vector2D) -> Vector2D:
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: Vector2D) -> Vector2D:
        return self + (-other)
    
    def __mul__(self, other: int) -> Vector2D:
        return Vector2D(self.x * other, self.y * other)
    
    def __rmul__(self, other: int) -> Vector2D:
        return self * other

    def __truediv__(self, other: int) -> Vector2D:
        return self * (1 / other)
    
    def __neg__(self) -> Vector2D:
        return Vector2D(-self.x, -self.y)
    
    def __eq__(self, other: Vector2D) -> bool:
        return self.x == other.x and self.y == other.y
    
    def __ne__(self, other: Vector2D) -> bool:
        return not self == other
    
    def __gt__(self, other: Vector2D) -> bool:
        return self.magnitude > other.magnitude
    
    def __ge__(self, other: Vector2D) -> bool:
        return self.magnitude >= other.magnitude
    
    def __lt__(self, other: Vector2D) -> bool:
        return self.magnitude < other.magnitude
    
    def __le__(self, other: Vector2D) -> bool:
        return self.magnitude <= other.magnitude
    
    def __repr__(self) -> str:
        return f'Vector2D({self.x}, {self.y})'
    
    def __str__(self) -> str:
        return f'({self.x}, {self.y})'
    
    def __getitem__(self, index: int) -> float:
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError(f'Index {index} out of bounds')
    
    def __setitem__(self, index: int, value: float) -> None:
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        else:
            raise IndexError(f'Index {index} out of bounds')
    
    def __iter__(self) -> Vector2D:
        return iter((self.x, self.y))
    
    def __len__(self) -> int:
        return 2
    
    def __bool__(self) -> bool:
        return self.magnitude != 0
