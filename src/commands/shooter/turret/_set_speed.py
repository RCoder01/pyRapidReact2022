import commands2

import subsystems


class SetSpeed(commands2.StartEndCommand):
    def __init__(self, speed: float):
        commands2.StartEndCommand(lambda: subsystems.shooter.turret.set_speed(speed), lambda: subsystems.shooter.turret.set_speed(0))
        self.setName("Set Turret Speed")
        self.addRequirements(subsystems.shooter.turret)
