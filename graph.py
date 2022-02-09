from __future__ import annotations
from multiprocessing import Pool
from datetime import datetime
import math
import collections

import numpy as np


Parameter = collections.namedtuple('Parameter', ['start', 'stop', 'inc'])


class Vector2D:
    def __init__(self, initial_x: float = 0, initial_y: float = 0) -> None:
        self.x = initial_x
        self.y = initial_y
    
    @property
    def magnitude(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5
    
    @magnitude.setter
    def magnitude(self, value: float) -> float:
        scale = value / self.magnitude
        self.x *= scale
        self.y *= scale
    
    @property
    def angle_radians(self) -> float:
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


class Range:
    def __init__(self, min: float, max: float) -> None:
        self.min = min
        self.max = max
    
    def __lt__(self, other: float) -> bool:
        return other < self.min
    
    def __le__(self, other: float) -> bool:
        return other <= self.min
    
    def __eq__(self, other: float) -> bool:
        return self.min <= other <= self.max
    
    def __ne__(self, other: float) -> bool:
        return not self == other
    
    def __ge__(self, other: float) -> bool:
        return other >= self.max
    
    def __gt__(self, other: float) -> bool: 
        return other > self.max



dt = 0.001
kd = 0.5*1.225*0.47*math.pi*(0.1143)**2/0.270
kg = 9.81

ROBOT_HEIGHT = 0.40

magvi = 8
initial_angle = 60

MAX_HEIGHT = 10

def made_goal(
        velocity_magnitude: float,
        angle: float,
        target_distance_center: float,
        target_height: float = 2.64,
        target_radius: float = 0.675,
        target_height_tolerance: float = 0.1143
        ) -> tuple[bool, float, tuple[Vector2D, Vector2D]]:
    target_distance = Range(target_distance_center - target_radius, target_distance_center + target_radius)
    target_height = Range(target_height, target_height + target_height_tolerance)
    vel = Vector2D()
    vel.magnitude = velocity_magnitude
    vel.angle_degrees = angle
    pos = Vector2D(0, ROBOT_HEIGHT)
    t = 0
    y_max = 0

    while t < 100: # not ((v[1] < 0 and p[1] < target_height + target_height_tolerance) or (p[1] >= 10 and p[0] > target_height + target_height_tolerance)):
        acc = vel.copy()
        acc *= -kd * acc.magnitude
        acc.y -= kg
        vel += acc * dt
        pos += vel * dt
        t += dt
        if pos.y > MAX_HEIGHT: # Ball exceeds height limit
            return False, pos.y, (vel, pos)
        if vel.y < 0: # Ball is falling
            if pos.y < target_height \
                    or pos.x > target_distance \
                    or pos.x * 2 < target_distance: # Ball is below target height or is past goal or is not far enough
                return False, y_max, (vel, pos)
            
            elif pos.x == target_distance and pos.y == target_height: # Ball is in goal
                return True, max(y_max), (vel, pos)
        
        else:
            y_max = vel.y
            if pos.y < target_height \
                    and pos.x > target_distance.min: # Ball is below target height and is past goal
                return False, y_max, (vel, pos)
    
    raise Exception('t exceeded limit of 100 seconds')


def iter(start, stop, inc):
    while True:
        if start >= stop:
            return start
        yield start
        start += inc

# print(made_goal(10, 30, 3))

# d = Parameter(3, 10, 0.05)
# theta = Parameter(30, 90, 0.1)
# dv = 0.1
# f = open("C:\\Users\\amumm\\Downloads\\data.txt", mode='w', encoding='UTF-8')
# for distance in iter(*d):
#     made_velocities = []
#     made_angles = []
#     for angle in iter(*theta):
#         # if angle % 1 == 0:
#         print(f'[{datetime.now()}]: testing distance={round(distance, 3)}, angle={round(angle, 3)}')
#         vi = dv
#         while (result := made_goal(vi, angle, distance))[1] <= 10:
#             vi += dv
#             if result[0]:
#                 made_velocities.append(round(vi, 3))
#                 made_angles.append(round(angle, 3))
#     f.write(f'{round(distance, 3)}\t{made_velocities}\t{made_angles}\n')

# Plot phistory on a graph
# plt.axis([0, max_val, 0, max_val])
# plt.scatter(made_velocities, made_angles, color="red")
# plt.xlabel("Velocity (m/s)")
# plt.ylabel("Angle (degrees)")
# plt.title("Ball trajectory")
# plt.show()

if __name__ == '__main__':
    # with Pool((d[1] - d[0]) / dd):
        pass
