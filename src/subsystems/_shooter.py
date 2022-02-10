import commands2
import wpilib

import constants
import utils.motor


class Shooter(commands2.SubsystemBase):

    def periodic(self) -> None:
        wpilib.SmartDashboard.putNumber('Shooter Speed', self.get_jeff())

        self._current_jeff = self._pid_controller.calculate(self.get_jeff())
        self._motors.set_velocity(self._current_jeff)

        return super().periodic()

    def simulationPeriodic(self) -> None:
        wpilib.SmartDashboard.putNumber('Jeff', self._current_jeff)
        return super().simulationPeriodic()

    def __init__(self) -> None:
        commands2.SubsystemBase.__init__(self)

        self._motors = utils.motor.HeadedDefaultMotorGroup(constants.Shooter.IDs)

        self._current_jeff = 0

    def get_jeff(self) -> float:
        """Returns the actual speed of the shooter motor."""
        return self._motors.get_lead_encoder_velocity() or 0

    def stop(self) -> None:
        self._current_jeff = 0
