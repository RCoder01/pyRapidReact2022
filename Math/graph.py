from __future__ import annotations
from multiprocessing import Pool
from datetime import datetime
import math
import collections
from typing import Any, Iterator

import matplotlib.pyplot as plt
import matplotlib.cm as cmx
import matplotlib.colors
import matplotlib
import numpy as np


Parameter = collections.namedtuple('Parameter', ['start', 'stop', 'inc'])


class Vector2D:
    __slots__ = ('x', 'y')

    def __init__(self, initial_x: float = 0, initial_y: float = 0) -> None:
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
    __slots__ = ('min', 'max')

    def __init__(self, min: float, max: float) -> None:
        self.min = min
        self.max = max
    
    def within(self, value: float) -> bool:
        return self.min <= value <= self.max


AIR_DENSITY = 1.225 # kg m^-3
DRAG_COEFFICIENT = 0.47
BALL_RADIUS = 0.1143 # m
CROSSSECTIONAL_AREA = math.pi*(BALL_RADIUS)**2 # m^2
BALL_MASS = 0.270 # kg

TARGET_HEIGHT = 2.64 # m
TARGET_HEIGHT_TOLERANCE = BALL_RADIUS # m
TARGET_RADIUS = 0.675 # m

MAX_HEIGHT = 10

ROBOT_HEIGHT = 0.40

dt = 0.001
kd = 0.5*AIR_DENSITY*DRAG_COEFFICIENT*CROSSSECTIONAL_AREA/BALL_MASS # m^-1
kg = 9.81

def made_goal(
        velocity_magnitude: float,
        angle: float,
        target_distance_center: float,
        target_height_min: float = TARGET_HEIGHT,
        target_radius: float = TARGET_RADIUS,
        target_height_tolerance: float = TARGET_HEIGHT_TOLERANCE,
        ) -> tuple[bool, bool | None, tuple[Any, ...]]:
    target_distance = Range(target_distance_center - target_radius, target_distance_center + target_radius)
    target_height = Range(target_height_min, target_height_min + target_height_tolerance)
    vel = Vector2D()
    vel.magnitude = velocity_magnitude
    vel.angle_degrees = angle
    pos = Vector2D(0, ROBOT_HEIGHT)
    t = 0
    y_max = 0

    while t < 100:
        acc = vel.copy()
        acc *= -kd * acc.magnitude
        acc.y -= kg
        vel += acc * dt
        pos += vel * dt
        t += dt
        if pos.y > MAX_HEIGHT: # Ball exceeds height limit
            return False, True, (pos.y, (vel, pos), 0)
        if vel.y < 0: # Ball is falling
            if pos.y < target_height.min \
                    or pos.x * 2 < target_distance.min: # Ball is below target height or is not far enough
                return False, False, (y_max, (vel, pos), 1)
            elif pos.x > target_distance.max: # Ball is past target distance
                return False, True, (y_max, (vel, pos), 2)
            
            elif target_distance.within(pos.x) and target_height.within(pos.y): # Ball is in goal
                return True, None, (y_max, (vel, pos), 3)
        
        else: # Ball is moving upwards
            y_max = pos.y
    
    raise Exception('t exceeded limit of 100 seconds')


def iter(start, stop, inc):
    while start <= stop:
        yield start
        start += inc


d = Parameter(3, 10, 0.1)
theta = Parameter(30, 90, 1)
dv = 0.5
# f = open("data.txt", mode='w', encoding='UTF-8')
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


def list_iter(list_: list) -> Iterator:
    for i in list_[:-1]:
        yield i
    return list_[-1]


def multi_iter(*args: Iterator[float]) -> Iterator[tuple[float, ...]]:
    if len(args) == 1:
        for i in args[0]:
            yield [i]
    else:
        list_ = list(multi_iter(*args[1:]))
        for i in args[0]:
            for j in list_:
                yield [i] + j


def single_run(d, theta):
    print(f'[{datetime.now()}]: testing distance={round(d, 3)}, angle={round(theta, 3)}')
    made_triplets = []
    if math.atan2(TARGET_HEIGHT, d - TARGET_RADIUS) > theta:
        return made_triplets
    vi = dv
    
    while not (result := made_goal(vi, theta, d))[1]:
        # print(vi, result)
        vi += dv
        if result[0]:
            made_triplets.append((round(d, 3), round(theta, 3), round(vi, 3)))
    
    return made_triplets

def angle_run(d):
    made_triplets = []
    for angle in iter(*theta):
        print(f'[{datetime.now()}]: testing distance={round(d, 3)}, angle={round(theta, 3)}')
        made_triplets += single_run(d, angle)
    return made_triplets

def calculate():
    with open(f"d={d.start, d.stop, d.inc};theta={theta.start, theta.stop, theta.inc}.txt", mode='a', encoding='UTF-8') as f:
        with Pool() as p:
            for triplet_set in p.starmap(single_run, multi_iter(iter(*d), iter(*theta))):
                f.write(f'{triplet_set}\n')

def graph_3d(data_fname: str):
    distances, angles, velocities = [], [], []
    with open(data_fname, mode='r', encoding='UTF-8') as f:
        for line in f:
            vals = eval(line)
            for d, t, v in vals:
                distances.append(d)
                angles.append(t)
                velocities.append(v)
    print(len(distances), len(velocities), len(angles))

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    cvar = velocities

    cm = plt.get_cmap('coolwarm')
    cNorm = matplotlib.colors.Normalize(vmin=min(cvar), vmax=max(cvar))
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cm)

    ax.scatter(distances, velocities, angles, c=scalarMap.to_rgba(cvar)) # , color="red"
    ax.set_xlabel("Distance (m)")
    ax.set_zlabel("Angle (degrees)")
    ax.set_ylabel("Velocity (m/s)")
    plt.title("Successfull shots")
    # plt.colorbar(scalarMap)
    plt.savefig("3d.png")
    plt.show()


def graph_12d(data_fname: str, *, cmap: str = 'viridis'):
    distances, angles, avg_velocities, range_velocities = [], [], [] , []
    with open(data_fname, mode='r', encoding='UTF-8') as f:
        for line in f:
            d, t, a, r = eval(line)
            distances.append(d)
            angles.append(t)
            avg_velocities.append(a)
            range_velocities.append(r)
    print(len(distances), len(angles), len(avg_velocities), len(range_velocities))

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    cvar = range_velocities

    cm = plt.get_cmap(cmap)
    cNorm = matplotlib.colors.Normalize(vmin=min(cvar), vmax=max(cvar))
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cm)

    ax.scatter(distances, avg_velocities, angles, c=scalarMap.to_rgba(cvar))
    ax.set_xlabel("Distance (m)")
    ax.set_zlabel("Angle (degrees)")
    ax.set_ylabel("Average Velocity (m/s)")
    plt.title("Successfull shots")
    plt.colorbar(scalarMap, label="Velocity Range (m/s)")
    plt.savefig("3d_avg.png")
    plt.show()


def average_2d(input_fname: str, output_fname: str):
    values: dict[tuple[float, float], list[float]] = {}
    num_datapoints = 0
    with open(input_fname, mode='r', encoding='UTF-8') as f:
        for line in f:
            vals = eval(line)
            for d, t, v in vals:
                key = (d, t)
                if key not in values:
                    values[key] = []
                values[key].append(v)
                num_datapoints += 1

    print(f'[{datetime.now()}]: compressing {num_datapoints} values')

    keys = sorted(list(values.keys()))

    with open(output_fname, mode='w', encoding='UTF-8') as f:
        for key in keys:
            vals = sorted(values[key])
            range_ = round(vals[-1] - vals[0], 5) # Assumes that for one angle, there's only one continuous range of velocities
            avg = round((vals[0] + vals[-1]) / 2, 5)
            f.write(f'{key + (avg, range_)}\n')

def average_1d(input_fname: str, output_fname: str):
    # Keys are distances
    # Values are dicts with keys of velocity-ranges and values of (angles, avg_velocity)
    values: dict[float, dict[float, tuple[float, float]]] = {}

    num_datapoints = 0
    with open(input_fname, mode='r', encoding='UTF-8') as f:
        for line in f:
            d, t, a, r = eval(line)
            if d not in values:
                values[d] = {}
            values[d][r] = (t, a)
            num_datapoints += 1

    print(f'[{datetime.now()}]: compressing {num_datapoints} values')

    keys = sorted(list(values.keys()))

    with open(output_fname, mode='w', encoding='UTF-8') as f:
        for key in keys:
            vals = values[key]
            max_range = max(vals.keys())
            f.write(f'{(key,) + vals[max_range] + (max_range,)}\n')


if __name__ == '__main__':
    # average_1d('Math/data3-2d.txt', 'Math/data3-1d.txt')
    graph_12d('Math/data3-1d.txt', cmap='cividis')
