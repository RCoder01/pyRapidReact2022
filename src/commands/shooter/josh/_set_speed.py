import commands2
import wpimath.controller

import subsystems


class SetSpeed(commands2.CommandBase):
    def __init__(self, josh: subsystems.shooter._josh.Josh, speed: float, PID_controller: wpimath.controller.PIDController, feedforward_constants, tolerance_constants) -> None:
        commands2.CommandBase.__init__(self)

        self._josh = josh

        self._pid_controller = PID_controller
        self._pid_controller.setTolerance(*tolerance_constants)

        self._feedforward = wpimath.controller.SimpleMotorFeedforwardMeters(
            feedforward_constants.S,
            feedforward_constants.V,
            feedforward_constants.A,
        )
        self._speed_setpoint = speed

    def initialize(self) -> None:
        self._pid_controller.setSetpoint(self._speed_setpoint)
        return super().initialize()

    def execute(self) -> None:
        self._josh.set_output(self.calculate_output())

    def calculate_output(self) -> float:
        output = 0
        output += self._pid_controller.calculate(self._josh.get_jeff(), self._speed_setpoint)
        output += self._feedforward.calculate(self._josh.get_jeff())
        return output

    def isFinished(self) -> bool:
        return self._pid_controller.atSetpoint()

    def end(self, interrupted: bool) -> None:
        self._josh.set_output(0)
        return super().end(interrupted)
