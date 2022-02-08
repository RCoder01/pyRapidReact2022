import matplotlib.pyplot as plt
import math

import numpy as np

dt = 0.001
kd = 0.04376
kg = 9.81

magvi = 8
initial_angle = 60
v = [magvi * math.cos(math.radians(initial_angle)), magvi * math.sin(math.radians(initial_angle))]
p = [0, 0.40]
t = 0
xh = []
yh = []

while v[1] > 0 or p[1] > 2.64:
    magv = math.sqrt(v[0]**2 + v[1]**2)
    theta = math.atan2(v[1], v[0])
    a = [-kd * magv**2 * math.cos(theta), -kd * magv**2 * math.sin(theta) - kg]
    v[0] += a[0] * dt
    v[1] += a[1] * dt
    p[0] += v[0] * dt
    p[1] += v[1] * dt
    t += dt
    xh.append(p[0])
    yh.append(p[1])
print(a, v, p, t)

# Plot phistory on a graph
max_val = max(max(xh), max(yh), 2.64)
plt.axis([0, max_val, 0, max_val])
plt.scatter(xh, yh, color="red")
plt.xlabel("X position (m)")
plt.ylabel("Y position (m)")
plt.title("Ball trajectory")
plt.show()