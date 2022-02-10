import math
import wpimath.controller
import matplotlib.pyplot as plt
import numpy as np

P, I, D = 1.2, 0.5, 2.1
dt = 0.02
VELOCITY_DECAY_RATE = 0#.015
SETPOINT = 50

controllerP = wpimath.controller.PIDController(P, 0, 0)
controllerI= wpimath.controller.PIDController(0, I, 0)
controllerD = wpimath.controller.PIDController(0, 0, D)
controllerPID = wpimath.controller.PIDController(P, I, D)
controllerPID.setTolerance(0.1, 0.01)

controllerP.setSetpoint(SETPOINT)
controllerI.setSetpoint(SETPOINT)
controllerD.setSetpoint(SETPOINT)
controllerPID.setSetpoint(SETPOINT)

controllerP.calculate(0)
controllerI.calculate(0)
controllerD.calculate(0)
controllerPID.calculate(0)

lx, lv, lp, li, ld, lpid = [], [], [], [] ,[], []
v = 0
x = 0
while not controllerPID.atSetpoint():
    lx.append(x / 10)
    lv.append(v)
    lp.append(controllerP.calculate(x))
    li.append(controllerI.calculate(x))
    ld.append(controllerD.calculate(x))
    lpid.append(controllerPID.calculate(x))
    v = min(max(v + min(max(lpid[-1], -1), 1) * dt, -10), 10)
    if v > 0:
        v = v - VELOCITY_DECAY_RATE
    else:
        v = v + VELOCITY_DECAY_RATE
    # v += lpid[-1] * dt
    if math.fabs(v) > 0.001:
        x += v * dt
    # print(x, lpid[-1])

# ld[0] = 0
# print(ld[:10])

# Graph the output of the controller on a matplotlib graph
plt.plot(np.arange(len(lx)), np.array(lx), color="yellow")
plt.plot(np.arange(len(lv)), np.array(lv), color="orange")
plt.plot(np.arange(len(lp)), np.array(lp), color="red")
plt.plot(np.arange(len(li)), np.array(li), color="green")
plt.plot(np.arange(len(ld)), np.array(ld), color="blue")
plt.plot(np.arange(len(lpid)), np.array(lpid), color="black")
plt.xlabel("Time (.02s)")
plt.ylabel("Output")
plt.title("PID Test")
# plt.yscale('log')

plt.savefig("PIDTest.png")

# i = 1
# while i < 100:
#     print(i, controllerI.calculate(i))
#     i *= 2

# for i in range(0, 100, 1):
#     print(controllerI.calculate(i))