from multiprocessing import Pool
from datetime import datetime
import math

dt = 0.001
kd = 0.5*1.225*0.47*math.pi*(0.1143)**2/0.270
kg = 9.81

ROBOT_HEIGHT = 0.40

magvi = 8
initial_angle = 60

def made_goal(velocity_magnitude, angle, target_distance, target_height=2.64, target_radius=0.675, target_height_tolerance=0.1143):
    v = [velocity_magnitude * math.cos(math.radians(angle)), velocity_magnitude * math.sin(math.radians(angle))]
    p = [0, ROBOT_HEIGHT]
    t = 0
    yh = []

    while not ((v[1] < 0 and p[1] < target_height + target_height_tolerance) or (p[1] >= 10 and p[0] > target_height + target_height_tolerance)):
        magv = math.sqrt(v[0]**2 + v[1]**2)
        theta = math.atan2(v[1], v[0])
        a = [-kd * magv**2 * math.cos(theta), -kd * magv**2 * math.sin(theta) - kg]
        v[0] += a[0] * dt
        v[1] += a[1] * dt
        p[0] += v[0] * dt
        p[1] += v[1] * dt
        t += dt
        yh.append(p[1])
    return (
        v[1] < 0 
        and target_distance - target_radius < p[0] < target_distance + target_radius
        and target_height <= p[1] <= target_height + target_height_tolerance,
        max(yh),
        (v, p)
    )


def iter(start, stop, inc):
    while True:
        if start >= stop:
            return start
        yield start
        start += inc

# print(made_goal(10, 30, 3))

d = [3, 10]
theta = (30, 90)
dv = 0.1
dtheta = 0.1
dd = 0.05
f = open("C:\\Users\\amumm\\Downloads\\data.txt", mode='w', encoding='UTF-8')
for distance in iter(3, 10, dd):
    made_velocities = []
    made_angles = []
    for angle in iter(30, 90, dtheta):
        # if angle % 1 == 0:
        print(f'[{datetime.now()}]: testing distance={round(distance, 3)}, angle={round(angle, 3)}')
        vi = dv
        while (result := made_goal(vi, angle, distance))[1] <= 10:
            vi += dv
            if result[0]:
                made_velocities.append(round(vi, 3))
                made_angles.append(round(angle, 3))
    f.write(f'{round(distance, 3)}\t{made_velocities}\t{made_angles}\n')

# Plot phistory on a graph
# plt.axis([0, max_val, 0, max_val])
# plt.scatter(made_velocities, made_angles, color="red")
# plt.xlabel("Velocity (m/s)")
# plt.ylabel("Angle (degrees)")
# plt.title("Ball trajectory")
# plt.show()
if __name__ == '__main__':
    with Pool((d[1] - d[0]) / dd):
        pass